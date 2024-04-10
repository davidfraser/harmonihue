#!/usr/bin/env python

import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = Axes3D(fig)
n_points = 240
theta = np.linspace(-np.pi, np.pi, n_points)
z = np.linspace(0, 0, n_points)
r = np.linspace(1, 1, n_points)
x = r * np.sin(theta)
y = r * np.cos(theta)
theta2 = np.linspace(0, 6*np.pi, n_points)
theta1 = np.linspace(0, 8*np.pi, n_points)
x1 = r * np.sin(theta)
y1 = r * np.cos(theta)
z1 = r * np.sin(theta1)
ax.plot(x, y, z, '-o', markevery=n_points/12, label='pythagorean circle')
ax.plot(x1, y1, z1, '-o', markevery=n_points/12, label='pythagorean spiral')
x2 = x1 * np.cos(theta1)
y2 = y1 * np.cos(theta1)
z2 = z1
ax.plot(x2, y2, z2, '-o', markevery=n_points/12, label='pythagorean spiral on sphere')
xtheta = np.linspace(0, 2*np.pi, n_points)
ytheta = np.linspace(0, 2*np.pi, n_points)
ztheta = np.linspace(0, 4*np.pi, n_points)
x3 = r * np.cos(xtheta) * np.cos(ztheta)
y3 = r * np.sin(xtheta) * np.cos(ztheta)
z3 = r * np.sin(ztheta)
# x3 = r * np.cos(xtheta) * np.sin(ytheta) * np.sin(ztheta)
# y3 = r * np.sin(xtheta) * np.cos(ytheta) * np.sin(ztheta)
# z3 = r * np.sin(xtheta) * np.sin(ztheta) * np.cos(ztheta)
# ax.plot(x3, y3, z3, '-o', markevery=n_points/12, label='pythagorean wrap')

# select which notes to write
nx, ny, nz = x1, y1, z1
notes = {}
for p in range(0, 12):
    i = p*n_points/12
    # notes[p] = a_x, a_y, a_z = x[i], y[i], z[i]
    notes[p] = a_x, a_y, a_z = nx[i], ny[i], nz[i]
    ax.text(a_x, a_y, a_z, str(p))
ax.legend()

for p in range(0, 12):
    a_x, a_y, a_z = notes[p]
    p_distance = []
    order = []
    for q in list(range(p, 12)) + list(range(0, p)):
        b_x, b_y, b_z = notes[q]
        d_x, d_y, d_z = (a_x-b_x), (a_y-b_y), (a_z-b_z)
        distance = math.sqrt(d_x*d_x + d_y*d_y + d_z*d_z)
        p_distance.append(distance)
        pq = (p+12-q) % 12
        s, pq = ("+", 12-pq) if pq > 6 else ("-", pq)
        order.append((distance, "d%02d%s" % (pq, s)))
    order.sort()
    print(" ".join("%0.2f" % d for d in p_distance) + " " + " ".join(label for d, label in order))

plt.show()

