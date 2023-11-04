// This file is part of the Acts project.
//
// Copyright (C) 2020 CERN for the benefit of the Acts project
//
// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

#include <fstream>

template <int spatialTrkGridSize, int temporalTrkGridSize, typename vfitter_t>
auto Acts::AdaptiveGridDensityVertexFinder<
    spatialTrkGridSize, temporalTrkGridSize,
    vfitter_t>::find(const std::vector<const InputTrack_t*>& trackVector,
                     const VertexingOptions<InputTrack_t>& vertexingOptions,
                     State& state) const
    -> Result<std::vector<Vertex<InputTrack_t>>> {
  // Remove density contributions from tracks removed from track collection
  if (m_cfg.cacheGridStateForTrackRemoval && state.isInitialized &&
      !state.tracksToRemove.empty()) {
    // Bool to check if removable tracks, that pass selection, still exist
    bool couldRemoveTracks = false;
    for (auto trk : state.tracksToRemove) {
      if (!state.trackSelectionMap.at(trk)) {
        // Track was never added to grid, so cannot remove it
        continue;
      }
      couldRemoveTracks = true;
      auto trackDensityMap = state.trackDensities.at(trk);
      m_cfg.gridDensity.subtractTrack(trackDensityMap, state.mainDensityMap);
    }
    if (!couldRemoveTracks) {
      // No tracks were removed anymore
      // Return empty seed, i.e. vertex at constraint position
      // (Note: Upstream finder should check for this break condition)
      std::vector<Vertex<InputTrack_t>> seedVec{vertexingOptions.constraint};
      return seedVec;
    }
  } else {
    state.mainDensityMap.clear();
    // Fill with track densities
    std::ofstream paramStream;
    paramStream.open("/home/frusso/hep/out/track_densities/trackParams.txt");
    std::ofstream covStream;
    covStream.open("/home/frusso/hep/out/track_densities/trackCovs.txt");
    for (auto trk : trackVector) {
      const BoundTrackParameters& trkParams = m_extractParameters(*trk);
      paramStream << trkParams.impactParameters() << "\n";
      covStream << trkParams.impactParameterCovariance().value() << "\n";
      // Take only tracks that fulfill selection criteria
      if (!doesPassTrackSelection(trkParams)) {
        if (m_cfg.cacheGridStateForTrackRemoval) {
          state.trackSelectionMap[trk] = false;
        }
        continue;
      }
      auto trackDensityMap =
          m_cfg.gridDensity.addTrack(trkParams, state.mainDensityMap);
      // Cache track density contribution to main grid if enabled
      if (m_cfg.cacheGridStateForTrackRemoval) {
        state.trackDensities[trk] = trackDensityMap;
        state.trackSelectionMap[trk] = true;
      }
    }
    paramStream.close();
    covStream.close();
    state.isInitialized = true;
    std::cout << "\nhi\n";
    saveDensityMap(state,
                   "/home/frusso/hep/out/track_densities/densities1D.txt");
  }

  double z = 0;
  double t = 0;
  double zWidth = 0;
  if (!state.mainDensityMap.empty()) {
    if (!m_cfg.estimateSeedWidth) {
      // Get z value of highest density bin
      auto maxZTRes = m_cfg.gridDensity.getMaxZTPosition(state.mainDensityMap);

      if (!maxZTRes.ok()) {
        return maxZTRes.error();
      }
      z = (*maxZTRes).first;
      t = (*maxZTRes).second;
    } else {
      // Get z value of highest density bin and width
      auto maxZTResAndWidth =
          m_cfg.gridDensity.getMaxZTPositionAndWidth(state.mainDensityMap);

      if (!maxZTResAndWidth.ok()) {
        return maxZTResAndWidth.error();
      }
      z = (*maxZTResAndWidth).first.first;
      t = (*maxZTResAndWidth).first.second;
      zWidth = (*maxZTResAndWidth).second;
    }
  }

  // Construct output vertex
  Vector4 seedPos =
      vertexingOptions.constraint.fullPosition() + Vector4(0., 0., z, t);

  Vertex<InputTrack_t> returnVertex = Vertex<InputTrack_t>(seedPos);

  SquareMatrix4 seedCov = vertexingOptions.constraint.fullCovariance();

  if (zWidth != 0.) {
    // Use z-constraint from seed width
    seedCov(2, 2) = zWidth * zWidth;
  }

  returnVertex.setFullCovariance(seedCov);

  std::vector<Vertex<InputTrack_t>> seedVec{returnVertex};

  return seedVec;
}

/// @brief function for saving a DensityMap
template <int spatialTrkGridSize, int temporalTrkGridSize, typename vfitter_t>
void Acts::AdaptiveGridDensityVertexFinder<
    spatialTrkGridSize, temporalTrkGridSize,
    vfitter_t>::saveDensityMap(const State& state,
                               const std::string& pathToFile) const {
  float spatialBinExtent = m_cfg.gridDensity.m_cfg.spatialBinExtent;
  float temporalBinExtent = m_cfg.gridDensity.m_cfg.temporalBinExtent;
  std::ofstream outstream;
  outstream.open(pathToFile);
  for (const auto& densityEntry : state.mainDensityMap) {
    Bin bin = densityEntry.first;
    float trackDensity = densityEntry.second;
    /*
    float z = m_cfg.gridDensity.getBinCenter(bin.first, spatialBinExtent);
    float t = 0.;
    if (temporalBinExtent > 0.) {
      t = m_cfg.gridDensity.getBinCenter(bin.second, temporalBinExtent);
    }
    */
    outstream << bin.first << " " << bin.second << " " << trackDensity << "\n";
  }
  outstream.close();
}

template <int spatialTrkGridSize, int temporalTrkGridSize, typename vfitter_t>
auto Acts::AdaptiveGridDensityVertexFinder<
    spatialTrkGridSize, temporalTrkGridSize,
    vfitter_t>::doesPassTrackSelection(const BoundTrackParameters& trk) const
    -> bool {
  // Get required track parameters
  const double d0 = trk.parameters()[BoundIndices::eBoundLoc0];
  const double z0 = trk.parameters()[BoundIndices::eBoundLoc1];
  // Get track covariance
  if (!trk.covariance().has_value()) {
    return false;
  }
  const auto perigeeCov = *(trk.covariance());
  const double covDD =
      perigeeCov(BoundIndices::eBoundLoc0, BoundIndices::eBoundLoc0);
  const double covZZ =
      perigeeCov(BoundIndices::eBoundLoc1, BoundIndices::eBoundLoc1);
  const double covDZ =
      perigeeCov(BoundIndices::eBoundLoc0, BoundIndices::eBoundLoc1);
  const double covDeterminant = covDD * covZZ - covDZ * covDZ;

  // Do track selection based on track cov matrix and d0SignificanceCut
  if ((covDD <= 0) || (d0 * d0 / covDD > m_cfg.d0SignificanceCut) ||
      (covZZ <= 0) || (covDeterminant <= 0)) {
    return false;
  }

  // Calculate track density quantities to check if track can easily
  // be considered as 2-dim Gaussian distribution without causing problems
  double constantTerm =
      -(d0 * d0 * covZZ + z0 * z0 * covDD + 2. * d0 * z0 * covDZ) /
      (2. * covDeterminant);
  const double linearTerm = (d0 * covDZ + z0 * covDD) / covDeterminant;
  const double quadraticTerm = -covDD / (2. * covDeterminant);
  double discriminant =
      linearTerm * linearTerm -
      4. * quadraticTerm * (constantTerm + 2. * m_cfg.z0SignificanceCut);
  if (discriminant < 0) {
    return false;
  }

  return true;
}
