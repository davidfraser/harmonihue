#!/usr/bin/env python

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = Axes3D(fig)
n_points = 120
theta = np.linspace(-np.pi, np.pi, n_points)
# z = np.linspace(2, 2, n_points)
z = np.linspace(0, 0, n_points)
r = np.linspace(1, 1, n_points)
# r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
z2 = z * np.sin(z)
ax.plot(x, y, z, '-o', markevery=n_points/12, label='pythagorean circle')
ztheta = np.linspace(0, 8*np.pi, n_points)
z2 = r * np.sin(ztheta)
ax.plot(x, y, z2, '-o', markevery=n_points/12, label='pythagorean spiral')
x2 = x * np.cos(ztheta)
y2 = y * np.cos(ztheta)
ax.plot(x2, y2, z2, '-o', markevery=n_points/12, label='pythagorean spiral on sphere')
ax.legend()

plt.show()

