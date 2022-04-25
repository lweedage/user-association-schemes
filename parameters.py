import math
from cycler import cycler
import matplotlib
import numpy as np

matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen',
                                                 'OrangeRed'])
colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100


def find_scenario(scenario):
    if scenario in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]:
        beamwidth_deg = 5
    elif scenario in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32]:
        beamwidth_deg = 10
    else:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4, 5, 6]:
        users_per_beam = 1
    elif scenario in [7, 8, 9, 10, 11, 12]:
        users_per_beam = 2
    elif scenario in [13, 14, 15, 16, 17, 18]:
        users_per_beam = 5
    elif scenario in [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
        users_per_beam = 10
    elif scenario in [31, 32, 33]:
        users_per_beam = 100
    else:
        users_per_beam = False

    if scenario in [1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21, 25, 26, 27, 31, 32, 33]:
        Penalty = True
    else:
        Penalty = False

    if scenario in [25, 26, 27, 28, 29, 30]:
        Clustered = True
    else:
        Clustered = False

    return beamwidth_deg, users_per_beam, Penalty, Clustered


scenario = int(input('Scenario?'))
# scenario = 1
beamwidth_deg, users_per_beam, Penalty, Clustered = find_scenario(scenario)

pi = math.pi
bs_of_interest = 10
radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

users = [int(i / (xDelta/1000 * yDelta/1000)) for i in [50, 500, 2500]]

beamwidth_u = 5

beamwidth_b = beamwidth_deg

W = 200  # in MHz  # bandwidth

if Penalty:
    M = 100000  # penalty on having disconnected users
else:
    M = 0


transmission_power = (10 ** 2.0) / (360 / beamwidth_deg)  # 30 dB
noise_figure = 7.8
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9) + noise_figure
noise = 10 ** (noise_power_db / 10)

BS_height = 10
user_height = 1.5
centre_frequency = 28e9
propagation_velocity = 3e8

SINR_min = 10 ** (5 / 10)

directions_bs = range(int(360 / beamwidth_b))
directions_u = range(int(360 / beamwidth_u))


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs


x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)

# iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}
# iterations = {10: 1, 100: 1000, 300: 334, 500: 200, 750: 133, 1000: 100}
iterations = {10: 1, 100: 500, 300: 167, 500: 100, 750: 67, 1000: 50}
# iterations = {10: 1, 100: 10, 300: 10, 500: 10, 750: 10, 1000: 10}
iterations = {60: 1, 601: 1, 3007: 1}

if beamwidth_b == 5:
    misalignment_user = {100: 1.9682613988252613, 300: 1.6317848174368959, 500: 1.4866377613013804,
                         750: 1.3799530202862103, 1000: 1.323930882575973}
    misalignment = {60: 1.7454759076711075, 601: 1.380565147312798, 3007: 1.2268435392410608}

elif beamwidth_b == 10:
    misalignment_user = {100: 2.2548903653685985, 300: 1.89158710623207, 500: 1.7428086785910102,
                         750: 1.6359443972910936, 1000: 1.580973055880226}
    misalignment = {60: 3.8995977190422626, 601: 2.875090051867872, 3007: 2.3221980422505157}

elif beamwidth_b == 15:
    misalignment_user = {100: 2.0109692232489222, 300: 1.7373935226648738, 500: 1.6415092020650677,
                         750: 1.56259471487693, 1000: 1.5111786912896545}
    misalignment = {60: 7.033445388403012, 601: 5.779474061814272, 3007: 5.2600395821014105}


RateRequirement = True
user_rate = 800  # Mbps

Torus = True

fading = np.random.normal(0, 4, (7000, number_of_bs))

