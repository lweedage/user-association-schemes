import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum
import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product
import initialization
from parameters import *
import functions as f

def find_distance_matrix(xu, yu, xbs, ybs):
    distance = np.zeros((len(xu), len(xbs)))
    for i in range(len(xu)):
        for j in range(len(xbs)):
            # x = np.minimum((xu[i] - xbs[j]) % xMax, (xbs[j] - xu[i]) % xMax)
            # y = np.minimum((yu[i] - ybs[j]) % yMax, (ybs[j] - yu[i]) % yMax)
            x = xu[i] - xbs[j]
            y = yu[i] - ybs[j]
            distance[i, j] = np.sqrt(x ** 2 + y ** 2)
    return distance

def number_of_connections(channel_capacity):
    connections = channel_capacity > 0
    connections = connections.astype(int)
    connections_per_bs = sum(connections)
    connections_per_user = sum(connections.transpose())
    return connections, connections_per_bs, connections_per_user


def optimization():
    alpha = input('Alpha = ')
    alpha = int(alpha)
    users = range(number_of_users)
    base_stations = range(number_of_bs)

    gain_bs = np.zeros((number_of_users, number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs, number_of_bs))
    power = np.zeros((number_of_users, number_of_bs))
    path_loss = np.zeros((number_of_users, number_of_bs))
    interference = np.zeros((number_of_users, number_of_bs, number_of_users, number_of_bs))

    for i in users:
        coords_i = f.user_coords(i)
        for j in base_stations:
            coords_j = f.bs_coords(j)
            for m in base_stations:
                coords_m = f.bs_coords(m)
                path_loss[i, m] = f.path_loss(coords_i, coords_m)
                for k in users:
                    coords_k = f.user_coords(k)
                    gain_bs[i, k, m] = f.find_gain(coords_m, coords_k, coords_m, coords_i, beamwidth_b)
                    gain_user[i, j, m] = f.find_gain(coords_i, coords_j, coords_i, coords_m, beamwidth_u)
                    if not (i == k and j == m):
                        interference[i, j, k, m] = transmission_power * gain_bs[i, k, m] * gain_user[i, j, m] / path_loss[i, m]
            power[i,j] = transmission_power * gain_bs[i, i, j] * gain_user[i, j, j] / path_loss[i,j]

    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.setParam('NonConvex', 2)
        m.Params.LogToConsole = 0

        # -------------- VARIABLES -----------------------------------
        x = {}
        SINR = {}
        SINR_user = {}
        I = {}
        I_inv = {}
        sigma_I = {}

        log_obj = {}

        maxmin_obj = {}
        angles_u = {}
        angles_bs = {}

        for i in users:
            for j in base_stations:
                x[i,j] = m.addVar(vtype = GRB.BINARY, name = f'x#{i}#{j}')
                SINR[i,j] = m.addVar(vtype = GRB.CONTINUOUS, name = f'SINR#{i}#{j}')
                I[i,j] = m.addVar(vtype = GRB.CONTINUOUS, name = f'I#{i}#{j}')
                sigma_I[i,j] = m.addVar(vtype = GRB.CONTINUOUS, name = f'sigma_I#{i}#{j}')
                I_inv[i,j] = m.addVar(vtype = GRB.CONTINUOUS, name = f'I_inv#{i}#{j}')
            SINR_user[i] = m.addVar(vtype= GRB.CONTINUOUS, name = f'SINR_user#{i}')
            if alpha == 1:
                log_obj[i] = m.addVar(vtype = GRB.CONTINUOUS, name = f'log_C_user#{i}')
            elif alpha == 2:
                maxmin_obj[i] = m.addVar(vtype= GRB.CONTINUOUS, name = f'maxmin_C_user#{i}')
        for j in base_stations:
            for d in directions_bs:
                angles_bs[j, d] = m.addVar(vtype= GRB.BINARY, name = f'angle_bs#{j}#{d}')
        for i in users:
            for d in directions_u:
                angles_u[i, d] = m.addVar(vtype=GRB.BINARY, name = f'angle_u#{i}#{d}')
        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        if alpha == 1:
            m.setObjective(quicksum(log_obj[i] for i in users), GRB.MAXIMIZE)
        elif alpha == 0:
            m.setObjective(quicksum(SINR_user[i] for i in users), GRB.MAXIMIZE)
        else:
            m.setObjective(1/(1-alpha) * quicksum(maxmin_obj[i] for i in users), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------
        # Define SINR and interference
        for i in users:
            for j in base_stations:
                m.addConstr(I[i, j] == quicksum(quicksum(x[k, m] * interference[i,j,k,m] for k in users if not (i == k and j == m)) for m in base_stations) , name=f'Interference#{i}#{j}')
                m.addConstr(sigma_I[i,j] == sigma + I[i,j], name = f'sigma_interference#{i}#{j}')
                m.addConstr(sigma_I[i,j] * I_inv[i, j] == 1, name=f'helper_constraint#{i}#{j}')
                m.addConstr(SINR[i,j] == x[i, j] * power[i, j] * I_inv[i,j], name=f'find_SINR#{i}#{j}')
            m.addConstr(SINR_user[i] == quicksum(1 + SINR[i,j] for j in base_stations), name = f'find_SINR_user#{i}')

        # Only 1 BS/User per angular direction
        for i in users:
            for d in directions_u:
                m.addConstr(angles_u[i, d] == quicksum(x[i,j] for j in base_stations if f.find_beam_number(f.find_bore(f.user_coords(i), f.bs_coords(j), beamwidth_u), beamwidth_u) == d), name = f'direction#{i}#{j}')
                m.addConstr(angles_u[i, d] <= 1)


        for j in base_stations:
            for d in directions_bs:
                m.addConstr(angles_bs[j, d] == quicksum(x[i,j] for i in users if f.find_beam_number(f.find_bore(f.bs_coords(j), f.user_coords(i), beamwidth_b), beamwidth_b) == d), name = f'direction#{i}#{j}')
                m.addConstr(angles_bs[j, d] <= 1)

        # Minimum SNR
        # for i in users:
        #     for j in base_stations:
        #       m.addConstr(SINR[i,j,t] >= x[i, j] * SINR_min, name = f'minimum_SNR#{i}#{j}#{t}')

        # Connections per BS
        for j in base_stations:
            m.addConstr(quicksum(x[i, j] for i in users) <= N_bs, name= f'connections_BS#{j}')

        # Connections per user
        for i in users:
            m.addConstr(quicksum(x[i,j] for j in base_stations) <= N_user, name=f'connections_user#{i}')

        # Rate requirement
        # for i in users:
        #     m.addConstr(quicksum(SINR[i,j] for j in base_stations) >= min_rate_SINR, name='rate_requirement')

        # at least 1 connection:
        for i in users:
            m.addConstr(quicksum(x[i,j] for j in base_stations) >= 1, name=f'1_con_user#{i}')


        if alpha == 1:
            for i in users:
                m.addGenConstrLog(SINR_user[i], log_obj[i], name=f'log_constraint#{i}')

        elif alpha >= 2:
            for i in users:
                m.addGenConstrPow(SINR_user[i], maxmin_obj[i], 1 - alpha, name = f'power_constraint#{i}')

        # --------------------- OPTIMIZE MODEL -------------------------
        # m.computeIIS()
        # m.write("IISmodel.lp")

        m.optimize()
        m.write("model.lp")
        m.getObjective()
        print('Objective value: %g' % m.objVal)




    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
        sys.exit()


    a = np.zeros((number_of_users, number_of_bs))
    total_SINR = np.zeros(number_of_users)
    interf = np.zeros((number_of_users, number_of_bs))
    angles = np.zeros((number_of_users, len(directions_u)))
    bs_angles = np.zeros((number_of_bs, len(directions_bs)))

    for i in range(number_of_users):
        total_SINR[i] = SINR_user[i].X

        for j in range(number_of_bs):
            a[i, j] = x[i, j].X
            interf[i,j] = SINR[i,j].X
        # for d in directions_u:
        #     angles[i, d] = angles_u[i,d].X
    # for j in range(number_of_bs):
    #     for d in directions_bs:
    #         bs_angles[j,d] = angles_bs[j,d].X
    # print(total_SINR)
    # print(interf)
    print('SINR sum:', sum(total_SINR), 'fairness =', f.fairness(total_SINR))
    return a, total_SINR

