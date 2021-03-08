from gurobipy import *
from parameters import Parameters

def optimal_sol(flows, switches):
    """
        Optimal:
        :param: flows: the list of flows,
        switches: the list of switches,
        :output:
        Performance parameters of Optimal
    """

    """Initialize the model"""
    m = Model("port_int")
    x = {}

    """Defining variables"""
    for w_id in switches:
        for p in switches[w_id].ports:
            x[w_id, p.id] = m.addVar(vtype=GRB.BINARY, name='x[%d,%d]' % (w_id, p.id))
    lambda_m = m.addVar(vtype=GRB.CONTINUOUS, name='lambda_m')

    """Constraint (2b)"""
    m.addConstrs(
        (
            quicksum(
                x[p.the_switch.id, p.id]
                for p in flows[f_id].ports
            ) >= 1
            for f_id in flows
        ), name="flow_converage"
    )

    """Constraint (2c)"""
    m.addConstrs(
        (
            quicksum(
                x[w_id, p.id] * p.rate
                for p in switches[w_id].ports
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
    # m.setParam("TIME_LIMIT", 10.0)
    m.optimize()
    if m.Status == 3:
        m.computeIIS()
        m.write("opt_model.ilp")

    """Saving output performance parameters in file"""
    fw = open('solutions/opt', 'w+')
    for w_id in switches:
        for p in switches[w_id].ports:
            if x[w_id, p.id].x == 1:
                fw.write(str(w_id) + ' ' + str(p.id) + '\n')
    fw.write(str(m.ObjVal) + '\n')
    f_obj = open("./solutions/obj.txt", "a")
    f_obj.write(str(m.ObjVal) + '\n')
    f_obj.close()
    fw.close()

