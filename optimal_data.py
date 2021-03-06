import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns
import math
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'xx-large',
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large',
        'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5',  '#96ACB7',  '#957D95'] * 100
markers = ['o', 'X', 'v' , 's', '*', 'P', '1', '+']

radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

users = [int(i / (xDelta / 1000 * yDelta / 1000)) for i in [100, 250, 500, 750, 1000]]
user_density = [100, 250, 500, 750, 1000]

M = 10000
beamwidth_deg = 10
s = 1
user_rate = 500

Shares = False



if Shares:
    x1 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(1) + str(user_rate) +  '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(2) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(5) + str(user_rate) + '.p'), 'rb')).values()
    x4 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(10) + str(user_rate) + '.p'), 'rb')).values()
    x5 = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(1000) + str(user_rate) + '.p'), 'rb')).values()

    # x1 = [i / j for i, j in zip(x1, users)]
    # x2 = [i / j for i, j in zip(x2, users)]
    # x3 = [i / j for i, j in zip(x3, users)]
    # x4 = [i / j for i, j in zip(x4, users)]
    # x5 = [i / j for i, j in zip(x5, users)]

    plt.plot(user_density, x1, '--', marker=markers[0], label='$s=1$', color=colors[0])
    plt.plot(user_density, x2, '--', marker=markers[1], label='$s=2$', color=colors[1])
    plt.plot(user_density, x3, '--', marker=markers[2], label='$s=5$', color=colors[2])
    plt.plot(user_density, x4, '--', marker=markers[3], label='$s=10$', color=colors[3])
    plt.plot(user_density, x5, '--', marker=markers[4], label='$s=\infty$', color=colors[4])

else:
    x1 = pickle.load(open(str('Data/Processed/cap' + str(5) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/cap' + str(15) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

    # x1 = [i / j for i, j in zip(x1, users)]
    # x2 = [i / j for i, j in zip(x2, users)]
    # x3 = [i / j for i, j in zip(x3, users)]

    plt.plot(user_density, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
    plt.plot(user_density, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
    plt.plot(user_density, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])


plt.xlabel('Users per km$^2$')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.show()


if Shares:
    x1 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(1) + str(user_rate) +  '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(2) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(5) + str(user_rate) + '.p'), 'rb')).values()
    x4 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(10) + str(user_rate) + '.p'), 'rb')).values()
    x5 = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(1000) + str(user_rate) + '.p'), 'rb')).values()

    plt.plot(user_density, x1, '--', marker=markers[0], label='$s=1$', color=colors[0])
    plt.plot(user_density, x2, '--', marker=markers[1], label='$s=2$', color=colors[1])
    plt.plot(user_density, x3, '--', marker=markers[2], label='$s=5$', color=colors[2])
    plt.plot(user_density, x4, '--', marker=markers[3], label='$s=10$', color=colors[3])
    plt.plot(user_density, x5, '--', marker=markers[4], label='$s=\infty$', color=colors[4])


else:
    x1 = pickle.load(open(str('Data/Processed/sat' + str(5) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x2 = pickle.load(open(str('Data/Processed/sat' + str(10) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    x3 = pickle.load(open(str('Data/Processed/sat' + str(15) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
    print(x2, x3)
    plt.plot(user_density, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
    plt.plot(user_density, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
    plt.plot(user_density, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])

plt.xlabel('Users per km$^2$')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.show()