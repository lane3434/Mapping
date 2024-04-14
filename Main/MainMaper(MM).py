import os
import math
import matplotlib.pyplot as plt
import numpy as np
import json

# Randomize grid dimensions (making it smaller)
grid_width = np.random.randint(3, 7)
grid_height = np.random.randint(3, 7)

# Randomize AI initial position within the grid
ai_pos = [np.random.randint(0, grid_width), np.random.randint(0, grid_height)]

# Function to generate a random goal position within the grid
def generate_goal_position():
    return [np.random.randint(0, grid_width), np.random.randint(0, grid_height)]

# Randomize initial goal position
goal_pos = generate_goal_position()

# Load or initialize AI brain
brain_json_path = 'C:/Users/LaneF/Downloads/Important/AAI/Mapping/Brain/Brain.JSON'

if os.path.exists(brain_json_path) and os.path.getsize(brain_json_path) > 0:
    with open(brain_json_path, 'r') as f:
        ai_brain = json.load(f)
else:
    ai_brain = {}

# Function to calculate Euclidean distance between two points
def euclidean_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Log distances to a file
def log_distance(distance):
    log_file_path = 'C:/Users/LaneF/Downloads/Important/AAI/Mapping/Logs/Location.txt'
    with open(log_file_path, 'a') as f:
        f.write(str(distance) + '\n')

# Log learning rates to a file
def log_learning_rate(learning_rate):
    log_file_path = 'C:/Users/LaneF/Downloads/Important/AAI/Mapping/Logs/log.txt'
    with open(log_file_path, 'a') as f:
        f.write(str(learning_rate) + '\n')

# Log map to a file
def log_map():
    map_file_path = 'C:/Users/LaneF/Downloads/Important/AAI/Mapping/Logs/Map.txt'
    with open(map_file_path, 'w') as f:
        # Write AI and goal positions
        f.write(f"AI position: {ai_pos}\n")
        f.write(f"Goal position: {goal_pos}\n")
        # Write grid dimensions
        f.write(f"Grid dimensions: {grid_width} x {grid_height}\n")

# Initialize visualization
plt.ion()
fig, ax = plt.subplots()

# Visualize the grid
ax.set_xticks(np.arange(0, grid_width, 1))
ax.set_yticks(np.arange(0, grid_height, 1))
ax.grid()

# Visualize the AI and the goal
ai_marker = ax.scatter(ai_pos[0], ai_pos[1], color='blue', label='AI')
goal_marker = ax.scatter(goal_pos[0], goal_pos[1], color='red', label='Goal')

# Update the visualization
plt.legend()
plt.draw()
plt.pause(0.1)

# Simulation parameters
learning_rate_decay = 0.9

# Simulate AI movement and learning
while True:
    # Use a decayed learning rate
    learning_rate = 0.1

    for _ in range(10):  # Repeat each iteration multiple times
        # Use AI brain to determine next move
        next_move = ai_brain.get(str(ai_pos), [np.random.randint(-1, 2), np.random.randint(-1, 2)])
        ai_pos[0] += next_move[0]
        ai_pos[1] += next_move[1]

        # Ensure AI stays within grid
        ai_pos[0] = max(0, min(grid_width - 1, ai_pos[0]))
        ai_pos[1] = max(0, min(grid_height - 1, ai_pos[1]))

        # Calculate distance to goal
        distance_to_goal = euclidean_distance(ai_pos, goal_pos)
        log_distance(distance_to_goal)

        # Update AI brain (simple learning: adjust next move based on distance to goal)
        ai_brain[str(ai_pos)] = [np.random.randint(-1, 2) * learning_rate, np.random.randint(-1, 2) * learning_rate]

        # Log learning rate
        log_learning_rate(learning_rate)

        # Update AI visualization
        ai_marker.set_offsets(ai_pos)
        plt.draw()
        plt.pause(0.5)  # Adjust the pause duration as needed

        # Log the map
        log_map()

    # Randomize goal position for the next iteration
    goal_pos = generate_goal_position()

    # Save AI brain to file
    with open(brain_json_path, 'w') as f:
        json.dump(ai_brain, f)
