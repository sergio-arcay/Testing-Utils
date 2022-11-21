"""

SOURCE:

    https://github.com/sergio-arcay/

SUMMARY:

    Build an animated scenario in a matplotlib window in which a specified number of balls fall, crash and bounce on the
    ground.

"""
import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import random


def generator_random_color():
    colors = list(mcolors.TABLEAU_COLORS.values())
    while 1:
        for color in random.sample(colors, len(colors)):
            yield color


# Acceleration due to gravity
g = 9.81

# The maximum range of ball's trajectory to plot.
XMAX = 5
YMAX = 4

# The coefficient of restitution for collisions. Collisions => floor, ceiling, side walls or other balls
uw = 0.8

# Friction coefficients
uk = 0.0004
us = 0.05

# Error distance
dd = 0.001

# The time step for the animation.
dt = 0.008

# Interval
interval = 1000*dt

# Color generator
random_colors = generator_random_color()


class Ball:
    def __init__(self, x0: float, y0: float, vx0: float, vy0: float, radius=0.08):
        self.x0 = max((min((XMAX-0.01, x0)), 0.01))
        self.y0 = max((min((YMAX-0.01, y0)), 0.01))
        self.vx0 = max((vx0, 0))
        self.vy0 = max((vy0, 0))
        self._x = self.x0
        self._y = self.y0
        self.vx = self.vx0
        self.vy = self.vy0
        self.radius = radius
        self.color = next(random_colors)
        self.plt_ball = plt.Circle(
            xy=(self.x0, self.y0), radius=radius, facecolor=self.color)
        self.collision_counter = 0
        self.scenario = None

    def state(self, t=0):
        while self.energy:
            t += dt

            self.x = self.x + self.vx * dt
            self.y = self.y + self.vy * dt

            if 0 < self.x < XMAX:
                self.vx = self.vx - self.vx * uk

            else:
                self.vx = -self.vx * uw
                self.collision_counter += 1

            if 0 < self.y < YMAX:
                self.vy = self.vy - dt * g - self.vy * uk

            else:
                self.vy = -self.vy * uw
                self.collision_counter += 1

            if self.y == 0 or self.y == YMAX or self.x == 0 or self.x == XMAX:
                self.vx -= self.vx * us
                self.vy -= self.vy * us

            if any(abs(self.x - ball.x) <= self.radius and abs(self.y - ball.y) <= self.radius for ball in self.scenario.balls if ball != self):
                self.vx = -self.vx * uw
                self.vy = -self.vy * uw
                self.collision_counter += 1

            yield self.energy

    def set_scenario(self, ball_scenario):
        self.scenario = ball_scenario

    @property
    def energy(self):
        return E if (E := (self.y * g + 0.5*self.vy**2 + 0.5*self.vx**2)) >= dd else 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value <= dd:
            self._x = 0
        elif value >= XMAX - dd:
            self._x = XMAX
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value <= dd:
            self._y = 0
        elif value >= YMAX - dd:
            self._y = YMAX
        else:
            self._y = value


class Scenario:
    def __init__(self, balls: list):
        self.balls = balls
        self.fig = None
        self.ax = None
        self.plt_bars = None
        self.xdata, self.ydata = [], []
        self.ani = None

    def run(self):
        # Set up a new Figure, with equal aspect ratio so the ball appears round.
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        # These are the objects we need to keep track of.
        for ball in self.balls:
            ball.set_scenario(self)
            self.ax.add_patch(ball.plt_ball)
        self.ani = animation.FuncAnimation(
            self.fig, self._animate, self._state, blit=False, interval=interval, repeat=False, init_func=self._init)
        return self

    def show(self):
        plt.show()
        return self

    def _state(self, t=0):
        """A generator yielding the ball's position at time t."""
        energetic_balls = self.balls.copy()
        while energetic_balls:
            for ball in energetic_balls:
                energy = next(ball.state(t))
                if not energy:
                    energetic_balls.remove(ball)
            yield self.balls

        self._finish()
        yield self.balls

    def _init(self):
        """Initialize the animation figure."""
        self.ax.set_xlim(0, XMAX)
        self.ax.set_ylim(0, YMAX)
        self.ax.set_xlabel('$x$ /m')
        self.ax.set_ylabel('$y$ /m')
        for ball in self.balls:
            ball.plt_ball.set_center((ball.x, ball.y))
        return map(lambda b: b.plt_ball, self.balls)

    def _animate(self, balls):
        """For each frame, advance the animation to the new position, pos."""
        for ball in balls:
            ball.plt_ball.set_center((ball.x, ball.y))
        return *map(lambda b: b.plt_ball, self.balls), *([self.ax.axis, *self.plt_bars] if self.plt_bars else [])

    def _finish(self):
        self.ax.get_yaxis().set_visible(False)
        max_collisions = max(ball.collision_counter for ball in self.balls)
        self.ax.set_xlabel('$x$ /collisions')
        self.plt_bars = plt.bar(x=[ball.x for ball in self.balls],
                                height=[(YMAX*ball.collision_counter/max_collisions) for ball in self.balls],
                                width=0.1,
                                color=[ball.color for ball in self.balls],
                                tick_label=[ball.collision_counter for ball in self.balls])


if __name__ == '__main__':

    falling_balls = [
        Ball(x0=0, y0=4, vx0=40, vy0=40),
        Ball(x0=0, y0=3, vx0=10, vy0=0),
        Ball(x0=0, y0=4, vx0=5, vy0=0),
        Ball(x0=1, y0=1, vx0=100, vy0=0),
    ]

    scenario = Scenario(falling_balls).run().show()
