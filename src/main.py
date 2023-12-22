import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from board import Board
from component import Component


# define range for input
bounds = [0, 100]
step_size = 1
body_list = []

x_size = 1500
y_size = 750

x_upper_lim = x_size
y_upper_lim = y_size


n_components = 1000
n_compToMove = 10
temp = 10000  # Same size for Temp and Iterations

initial_population = 100
every = 100

for n in range(n_components):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    body_list.append(
        Component(
            random.randint(0.1 * x_size, 0.9 * x_size),
            random.randint(0.1 * y_size, 0.9 * y_size),
            7.5,
            5,
            r,
            g,
            b,
        )
    )

dummyPCB = Board(body_list, y_size, x_size, bounds, step_size, temp)
initial_dist = dummyPCB.total_dist

initial_pop = body_list[0:initial_population]
PCB = Board(initial_pop, y_size, x_size, bounds, step_size, temp)
PCB.resolve_overlap()

fig, ax = plt.subplots(figsize=(15, 7.5))


def draw_frame(i):
    increment = 10
    ax.clear()
    ax.set_xlim(0, x_size)
    ax.set_ylim(0, y_size)
    ax.set_aspect('equal', adjustable='box')

    # Update PCB for the current frame
    curr_size = initial_population + int(increment * (i - every) / every)
    if i != 0 and i % every == 0 and curr_size < len(body_list):
        if curr_size + increment > len(body_list):
            increment = len(body_list) - curr_size
        PCB.body_list.extend(body_list[curr_size:curr_size + increment])
        PCB.resolve_overlap()
    
    PCB.draw(ax)  # Assuming PCB has a draw method to draw on matplotlib axes

    # Additional console output, if needed
    if i == temp - 1:
        print("Improved by {}".format(initial_dist - PCB.total_dist))

# Create the animation
ani = animation.FuncAnimation(fig, draw_frame, frames=temp, interval=10)

# Display the animation
plt.show()
