"""

SOURCE:

    https://www.youtube.com/watch?v=xEhgxJcH5hk/

"""


import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

fps = 10
frn = fps*6
N = 250

x = np.linspace(-4, 4, N+1)
X, Y = np.meshgrid(x, x)
z_array = np.zeros((N+1, N+1, frn))


def f(X, Y, sigma):
    return 1/np.sqrt(sigma)*np.exp(-(X**2+Y**2)/sigma**2)


def animate(i, z_array, plot):
    plot[0].remove()
    sigma = 1.5 + np.sin(i*2*np.pi/frn)
    z_array[:, :, i] = f(X, Y, sigma)
    plot[0] = ax.plot_surface(X, Y, z_array[:, :, i], cmap="magma")


plot = [ax.plot_surface(X, Y, z_array[:, :, 0])]
ax.set_zlim(0, 1.2)
anim = animation.FuncAnimation(fig, animate, frn, fargs=(z_array, plot), interval=1000/fps)
# anim.save("animation3d.gif", fps=fps)
plt.show()
