import numpy as np
import random
import math


class Boid:
    def __init__(self, label):
        self.x = random.randrange(100, 900)
        self.y = random.randrange(100, 900)
        self.angle = random.uniform(0.0, 2.0 * math.pi)
        self.label = label
        self.color = "black"
        self.positions = Boid.new_flock(100, np.array([100, 900]), np.array([200, 1100]))
        self.velocities = Boid.new_flock(100, np.array([0, -20]), np.array([10, 20]))

    def draw_boid(self, canvas):
        size = 18
        x1 = self.x + size * math.cos(self.angle)
        x2 = self.y + size * math.sin(self.angle)
        canvas.create_line(
            self.x, self.y, x1, x2, fill="black", arrow="last", arrowshape=(12.8, 16, 4.8), width=2, tags=self.label
        )

    def flock(self, canvas, screen_size):
        distance = 3
        # calculate next the drone moves to
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        # when drone goes off screen, will come back from other side of screen
        self.x = self.x % screen_size
        self.y = self.y % screen_size
        canvas.delete(self.label)
        self.draw_boid(canvas)

    def euclidean_distance(self, neighbour_boid):
        return math.sqrt(
            (self.x - neighbour_boid.x) * (self.x - neighbour_boid.x)
            + (self.y - neighbour_boid.y) * (self.y - neighbour_boid.y)
        )

    @staticmethod
    def new_flock(count, lower_limits, upper_limits):
        width = upper_limits - lower_limits
        return lower_limits[:, np.newaxis] + np.random.rand(2, count) * width[:, np.newaxis]

    @staticmethod
    def animate(frame):
        boid.update_boids()
        scatter.set_offsets(boid.positions.transpose())


def animate_boid(boid):
    import matplotlib.pyplot as plt
    from matplotlib import animation

    figure, axes = plt.subplots()
    axes.set_visible(False)
    scatter = axes.scatter([0, 2000], [0, 2000], marker="d", edgecolor="k", lw=0.5)

    def animate(frame):
        boid.update_boids()
        scatter.set_offsets(boid.positions.transpose())

    anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)
    return anim.to_jshtml()
