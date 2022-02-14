import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle
import find_data

# k = int(input('k ='))


def find_sorted_users(bs, x_user, y_user):
    # on a torus
    x = np.minimum((x_user - bs[0]) % xDelta, (bs[0] - x_user) % xDelta)
    y = np.minimum((y_user - bs[1]) % yDelta, (bs[1] - y_user) % yDelta)
    return np.argsort(x ** 2 + y ** 2)

def find_closest(user):
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.argsort(x**2 + y**2)[:k]

def find_closest_snr(user, x_user, y_user):
    snr = []
    for bs in range(number_of_bs):
        snr.append(f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr)[:k]


for number_of_users in [100, 300, 500, 750, 1000]:
    for k in [1, 2, 3, 4, 5]:
        optimal = []
        xs = []
        ys = []
        name = str('MC_closest_heuristic_k=' + str(k) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

        iteration_min, iteration_max = 0, iterations[number_of_users]
        failed_link_constraints = []
        failed_sinr_constraints = []

        for iteration in range(iteration_min, iteration_max):
            opt_x = np.zeros((number_of_users, number_of_bs))
            print('Iteration ', iteration)
            np.random.seed(iteration)
            x_user, y_user = f.find_coordinates(number_of_users)

            for u in range(number_of_users):
                bs = find_closest_snr(u, x_user, y_user)
                for b in bs:
                    snr = f.find_snr(u, b,  x_user, y_user)
                    if snr > SINR_min:
                        opt_x[u, b] = 1

            link_constraint_fails = 0
            links_per_user = sum(np.transpose(opt_x))

            for u in range(number_of_users):
                if links_per_user[u] == 0:
                    link_constraint_fails += 1

            failed_link_constraints.append(link_constraint_fails)
            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
        disconnected = [0 for i in range(iteration_max)]
        find_data.main(optimal, xs, ys, disconnected, SNRHeuristic = True, k = k)