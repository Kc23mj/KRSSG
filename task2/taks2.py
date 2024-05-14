import cv2
import numpy as np

# Load the image
image = cv2.imread('/mnt/data/Image1 (1).png')

# Convert image to grayscale and binary format
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find start (green) and goal (red) positions
start_position = None
goal_position = None

for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        if (image[y, x] == [0, 255, 0]).all():  # Green
            start_position = (x, y)
        elif (image[y, x] == [0, 0, 255]).all():  # Red
            goal_position = (x, y)

print(f"Start position: {start_position}")
print(f"Goal position: {goal_position}")

from ompl import base as ob
from ompl import geometric as og

# Define the state space (2D)
space = ob.RealVectorStateSpace(2)

# Set the bounds of the space
bounds = ob.RealVectorBounds(2)
bounds.setLow(0)
bounds.setHigh(0, binary_image.shape[1])
bounds.setHigh(1, binary_image.shape[0])
space.setBounds(bounds)

# Define the SimpleSetup
ss = og.SimpleSetup(space)

# Define the validity checker
def is_state_valid(state):
    x, y = int(state[0]), int(state[1])
    return binary_image[y, x] == 255

ss.setStateValidityChecker(ob.StateValidityCheckerFn(is_state_valid))

# Set the start and goal states
start = ob.State(space)
goal = ob.State(space)
start[0], start[1] = start_position
goal[0], goal[1] = goal_position

ss.setStartAndGoalStates(start, goal)

# Use BIT* algorithm
planner = og.BITstar(ss.getSpaceInformation())
ss.setPlanner(planner)

# Try to solve the problem
solved = ss.solve(1.0)

if solved:
    path = ss.getSolutionPath()
    path.interpolate()  # Interpolate the path for smoothness
    print("Found solution:")
else:
    print("No solution found")

if solved:
    path_states = path.getStates()
    for state in path_states:
        x, y = int(state[0]), int(state[1])
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)  # Draw the path points

    # Display the resulting image
    cv2.imshow('Path', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Path could not be found.")


