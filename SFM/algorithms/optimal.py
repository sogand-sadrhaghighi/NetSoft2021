from gurobipy import *

def optimal_sol(flows, switches):
    """
        Optimal:
        :param: flows: the list of flows,
        switches: the list of switches,
        :output:
        Performance parameters of Optimal
    """

    """Initialize the model"""
    m = Model("flow_frac")
    z = {}

    """Defining variables"""
    for w_id in switches:
        for f in switches[w_id].flows:
            z[f.id, w_id] = m.addVar(vtype=GRB.BINARY, name='z[%d,%d]' % (f.id, w_id))
    lambda_m = m.addVar(vtype=GRB.CONTINUOUS, name='lambda_m')

    """Constraint (2b)"""
    m.addConstrs(
        (
            quicksum(
                z[f_id, w.id]
                for w in flows[f_id].switches
            ) == 1
            for f_id in flows
        ), name="flow_converage"
    )

    """Constraint (2c)"""
    m.addConstrs(
        (
            quicksum(
                z[f.id, w_id] * f.rate
                for f in switches[w_id].flows
            ) <= lambda_m
            for w_id in switches
        ), name="switch_capacity_2"
    )

    """Define objective"""
    m.setObjective(
        lambda_m, GRB.MINIMIZE
    )

    """Defining solver parameters"""
    m.setParam("LogToConsole", False)
    m.optimize()

    """Saving output performance parameters in file"""
    f_opt = open('solutions/opt', 'w+')
    for w_id in switches:
        for f in switches[w_id].flows:
            if z[f.id, w_id].x == 1:
                f_opt.write(str(f.id) + ' ' + str(w_id) + '\n')
    f_opt.write(str(m.ObjVal) + '\n')
    f_opt.close()
    f_obj = open("./solutions/obj.txt", "a")
    f_obj.write(str(m.ObjVal) + '\n')
    f_obj.close()
