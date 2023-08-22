#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

import acts
from acts.examples import (
    Sequencer,
    ParticleSelector,
    TrackParameterSelector,
)
from acts.examples.simulation import addPythia8
from acts.examples.reconstruction import (
    addVertexFitting,
    VertexFinder,
)

u = acts.UnitConstants


def runVertexFitting(
    field,
    outputDir: Path,
    outputRoot: bool = True,  # TODO: You don't really need this boolean, you can just write outputDir = None if you don't want to save the result
    inputParticlePath: Optional[Path] = None,
    inputTrackSummary: Path = None,
    vertexFinder: VertexFinder = "AMVF",  # VertexFinder.Truth,
    s=None,
):
    s = s or Sequencer(events=100, numThreads=-1)

    logger = acts.logging.getLogger("VertexFittingExample")

    inputParticles = "particles_input"
    if inputParticlePath is None:
        logger.error("Please provide a path to the truth information.")
        return
    logger.info("Reading particles from %s", inputParticlePath.resolve())
    assert inputParticlePath.exists()
    s.addReader(
        acts.examples.RootParticleReader(
            level=acts.logging.INFO,
            filePath=str(inputParticlePath.resolve()),
            particleCollection=inputParticles,
            orderedEvents=False,
        )
    )

    # TODO: Here you can apply cuts to the truth particles (you need to modify the parameters to suit your needs)
    selectedParticles = "particles_selected"
    ptclSelector = ParticleSelector(
        level=acts.logging.INFO,
        inputParticles=inputParticles,
        outputParticles=selectedParticles,
        removeNeutral=True,
        absEtaMax=2.5,  # 2.5
        rhoMax=999999.0 * u.mm,
        ptMin=0 * u.MeV,
    )
    s.addAlgorithm(ptclSelector)

    trackParameters = "fittedTrackParameters"

    if inputTrackSummary is None:
        logger.error("Please provide a path to the input track summary.")
        return
    logger.info("Reading track summary from %s", inputTrackSummary.resolve())
    assert inputTrackSummary.exists()
    associatedParticles = "associatedTruthParticles"
    trackSummaryReader = acts.examples.RootTrajectorySummaryReader(
        level=acts.logging.VERBOSE,
        outputTracks=trackParameters,
        outputParticles=associatedParticles,
        filePath=str(inputTrackSummary.resolve()),
        orderedEvents=False,
    )
    s.addReader(trackSummaryReader)

    # TODO: Here you can apply cuts to the track parameters (you need to modify the parameters to suit your needs)
    trackParamSelector = TrackParameterSelector(
        level=acts.logging.INFO,
        inputTrackParameters=trackSummaryReader.config.outputTracks,
        outputTrackParameters="selectedTrackParameters",
        absEtaMax=100,
        loc0Max=1000.0 * u.mm,  # rho max
        ptMin=0.0 * u.MeV,
    )
    s.addAlgorithm(trackParamSelector)
    trackParameters = trackParamSelector.config.outputTrackParameters

    logger.info("Using vertex finder: %s", vertexFinder.name)

    addVertexFitting(
        s,
        field,
        trackParameters=trackParameters,
        associatedParticles=inputParticles,
        trajectories=None,
        vertexFinder=vertexFinder,
        outputDirRoot=outputDir if outputRoot else None,
    )

    return s


if "__main__" == __name__:
    # TODO: Did you run a simulation without B field? If not, you need to provide the correct field here.
    field = acts.ConstantBField(acts.Vector3(0, 0, 0 * u.T))

    inputParticlePath = Path("/home/frusso/hep/out/billy/particles_python.root")
    if not inputParticlePath.exists():
        print("Fatal: Input particle path does not exist.")
        quit()

    inputTrackSummary = Path("/home/frusso/hep/out/billy/tracksummary_python.root")
    if not inputTrackSummary.exists():
        print("Fatal: Input track summary path does not exist.")
        quit()

    outputDir = Path("/home/frusso/hep/out/billy/")
    runVertexFitting(
        field,
        vertexFinder=VertexFinder.Iterative,
        inputParticlePath=inputParticlePath,
        inputTrackSummary=inputTrackSummary,
        outputDir=outputDir,
    ).run()
