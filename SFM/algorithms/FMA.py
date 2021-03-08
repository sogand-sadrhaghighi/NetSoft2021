from gurobipy import *
import numpy as np
import networkx as nx

def fms_sol(flows, switches, delta):
    """
        FMA:
        :param: flows: the list of flows,
        switches: the list of switches,
        delta: parameter epsilon
        :output:
        Performance parameters of FMA
    """
    """Initializing the variables"""
    lambda_u = max([w.get_total_traffic() for w in switches.values()])
    lambda_l = max([f.rate for f in flows.values()])
    lambda_m = lambda_u
    best_z = {}
    best_l = {}
    best_lambda_m = lambda_u

    """Set the parameters of the solver"""
    setParam('Threads', 16)

    """Solve the LP version of the problem"""
    while lambda_u - lambda_l > delta:
        m = Model("flow_frac")
        z = {}
        l = {}
        for w_id in switches:
            for f in switches[w_id].flows:
                z[f.id, w_id] = m.addVar(vtype=GRB.CONTINUOUS, name='z[%d,%d]' %(f.id, w_id))
            l[w_id] = m.addVar(vtype=GRB.CONTINUOUS, name='l[%d]' %w_id)

        """Relaxed version of constraint 2b"""
        m.addConstrs(
            (
                quicksum(
                    z[f_id, w.id]
                    for w in flows[f_id].switches
                ) == 1
                for f_id in flows
            ), name="flow_converage"
        )

        """Relaxed version of constraint 2c"""
        m.addConstrs(
            (
                quicksum(
                    z[f.id, w_id]
                    for f in switches[w_id].flows
                ) == l[w_id]
                for w_id in switches
            ), name="switch_capacity_1"
        )
        m.addConstrs(
            (
                quicksum(
                    z[f.id, w_id] * f.rate
                    for f in switches[w_id].flows
                ) <= lambda_m
                for w_id in switches
            ), name="switch_capacity_2"
        )
        """Find the objective of LP"""
        m.setObjective(
            0, GRB.MINIMIZE
        )
        m.setParam("LogToConsole", False)
        m.optimize()
        if m.Status == 2:
            lambda_u = lambda_m
            best_z = z
            best_l = l
            if lambda_m < best_lambda_m:
                best_lambda_m = lambda_m
                for w_id in switches:
                    for f in switches[w_id].flows:
                        best_z[f.id, w_id] = z[f.id, w_id].x
                    #
                    best_l[w_id] = l[w_id].x
        else:
            lambda_l = lambda_m
        lambda_m = (lambda_u + lambda_l) / 2.0

    G = nx.Graph()
    for f in flows.values():
        G.add_node('f_%d' %f.id)
    for w in switches.values():
        kw = int(np.ceil(best_l[w.id]))
        if kw == 0:
            continue
        for s in range(1, kw+1):
            G.add_node('w_%d_%d' %(w.id, s))
        s = 1
        s_itr = 0.0
        for f in w.get_sorted_flows():
            if s > kw:
                break
            if best_z[f.id, w.id] <= 0:
                continue
            if best_z[f.id, w.id] + s_itr >= 1:
                G.add_edge('w_%d_%d'%(w.id, s), 'f_%d' %f.id, weight=(1-s_itr))
                s += 1
                s_itr = best_z[f.id, w.id] + s_itr - 1
                if s_itr > 0:
                    G.add_edge('w_%d_%d' % (w.id, s), 'f_%d' % f.id, weight=s_itr)
            else:
                G.add_edge('w_%d_%d' % (w.id, s), 'f_%d' % f.id, weight=best_z[f.id, w.id])
                s_itr += best_z[f.id, w.id]
    #
    res = nx.max_weight_matching(G, maxcardinality=True)
    f_approx = open('solutions/approx', 'w+')
    approx_obj = {}
    for mathced in res:
        if mathced[0][0] == 'f':
            f = mathced[0].split('_')[-1]
            w = mathced[1].split('_')[1]
            f_approx.write(f + ' ' + w + '\n')
        else:
            f = mathced[1].split('_')[-1]
            w = mathced[0].split('_')[1]
            f_approx.write(f + ' ' + w + '\n')
        #
        if w not in approx_obj:
            approx_obj[w] = flows[int(f)].rate
        else:
            approx_obj[w] += flows[int(f)].rate
            
    """Saving output performance parameters in file"""
    f_approx.write(str(max(approx_obj.values())) + '\n')
    f_approx.close()
    f_obj = open("./solutions/obj.txt", "a")
    f_obj.write(str(max(approx_obj.values())) + '\n')
    f_obj.close()
