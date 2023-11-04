import matplotlib.pyplot as plt
import numpy as np

# Your data
x_values = [0, 0, 0, 0, 0]  # Replace with your actual x-values
y_values = [0, 1, 2, 3, 4]  # Replace with your actual y-values
density = [0.1 ,0.2, 0.3, 0.2, 0.1]  # Replace with your actual density values

# Define marker size in the x-direction
marker_size_x = 100  # Adjust as needed

# Calculate marker size in the y-direction
# You can adjust this calculation based on your data
marker_size_y = np.array([marker_size_x * abs(y - 0) for y in y_values])

# Create the scatter plot with different marker sizes
plt.scatter(x_values, y_values, c=density, cmap='viridis', s=marker_size_y, marker='o')  # Modify the cmap and marker type as needed

# Set the x-axis limit to zoom in
plt.xlim(0, max(x_values))  # Adjust max(x_values) as needed to fit your data

# Adjust aspect ratio
plt.gca().set_aspect('equal')

# Disable autoscaling for the y-axis
plt.autoscale(enable=True, axis='y')

# Add labels and title
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Scatter Plot with Zoomed X-axis and Different Marker Sizes')

# Show the plot
plt.savefig("/home/frusso/hep/out/track_densities/try.pdf")