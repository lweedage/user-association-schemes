import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle
import matplotlib as mpl
import seaborn as sns

# plt.rcParams["figure.figsize"] = (4, 5)
bs = 0
delta = 1

# number_of_users = int(input('Number of users?'))

for number_of_users in [100, 300, 500, 750, 1000]:
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    Heuristic = False
    SNRHeuristic = False
    User_Heuristic = False
    GreedyRate = False
    GreedyHeuristic = False

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
        np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(users_per_beam))

    if Heuristic:
        if User_Heuristic:
            name = str('beamwidth_user_heuristic' + name)
        else:
            name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    elif GreedyRate:
        name = str(name + 'GreedyRate')
    elif GreedyHeuristic:
        name = str(name + 'GreedyHeuristic')

    if Clustered:
        name = str(name + '_clustered')

    grid_bs = pickle.load(open(str('Data/grid_bs_' + name + '.p'), 'rb'))
    grid_mc = pickle.load(open(str('Data/grid_mc_' + name + '.p'), 'rb'))

    total_visits = pickle.load(open(str('Data/grid_total_visits_' + name + '.p'), 'rb'))

    x_large = [x * delta for x in x_bs]
    y_large = [y * delta for y in y_bs]

    xmax = int(np.ceil(xmax))
    ymax = int(np.ceil(ymax))

    values = range(0, xmax + 1, 10)
    real_value = range(0, xmax * delta + 1, 10 * delta)

    values_y = range(0, ymax + 1, 10)
    real_value_y = range(0, ymax * delta + 1, 10 * delta)

    cmap = sns.color_palette("Blues", as_cmap=True)
    norm = mpl.colors.Normalize(vmin=0, vmax=1)

    fig, ax = plt.subplots()
    plt.imshow(grid_bs / total_visits, cmap=cmap)
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))
    plt.scatter(x_large, y_large, color='k', marker='o')
    plt.scatter(x_large[bs_of_interest], y_large[bs_of_interest], color='red', marker='o')
    # plt.xticks(real_value, values)
    # plt.yticks(real_value_y, values_y)
    # plt.title("Where do users have MC?")

    plt.savefig(str('Figures/heatmap_bs' + name + '.png'), dpi=300)
    # plt.show()

    fig, ax = plt.subplots()
    plt.imshow(grid_mc / total_visits, cmap=cmap)
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))
    plt.scatter(x_large, y_large, color='k', marker='o')
    # plt.xticks(real_value, values)
    # plt.yticks(real_value_y, values_y)
    # plt.title("Where do users have MC?")

    plt.savefig(str('Figures/heatmap_mc' + name + '.png'), dpi=300)
    # plt.show()
