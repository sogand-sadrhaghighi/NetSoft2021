from time import time
from generators import get_topo, get_rand_flows, write_scenario_to_file, read_flows, write_fat_tree_to_file
from algorithms.optimal import optimal_sol
from algorithms.PMA import pd_sol
from algorithms.planck import planck
import optparse
import numpy as np
from generators import mininet_read_flows

if __name__ == '__main__':
    """Network and flow specifications"""
    capacity=100
    parser = optparse.OptionParser()
    """Specify the topology from network folder"""
    parser.add_option('-t', '--topo',
                      action="store", dest="topo_name",
                      help="topo file name in network dir", default="fattree2")
    """ Specifiy the number of flows """
    parser.add_option('-f', '--flow',
                      action="store", dest="flow_num",
                      help="number of flows", default="10")
    """ Specifiy the flow rate range """
    parser.add_option('-l', '--fmin',
                      action="store", dest="min_rate",
                      help="minimum flow rate", default="50") #0.2  #0.6 (main)
    parser.add_option('-u', '--fmax',
                      action="store", dest="max_rate",
                      help="maximum flow rate", default="200") #0.6   #2.0 (main)
    """The flow rate can be entered as an input file"""
    parser.add_option('-i', '--iflows',
                      action="store", dest="input_flows_name",
                      help="input flows file name in network dir", default="")

    """Convert the arguments to numeric format"""
    options, args = parser.parse_args()
    topo_name = options.topo_name
    flow_num = int(options.flow_num)
    min_rate = float(options.min_rate)
    max_rate = float(options.max_rate)
    input_flows_file = options.input_flows_name

    """Reading the flows from a file/Generating flows randomly"""
    topo, switches, endpoints = get_topo(topo_name)
    #mininet_flows=mininet_read_flows('planckflow.txt',switches,topo)
    if input_flows_file == "":
        flows = get_rand_flows(topo, switches, endpoints, flow_num, min_rate, max_rate)
    else:
        flows = read_flows(input_flows_file, switches)
    write_scenario_to_file(switches, flows)


    """
    Calling the algorithms
    Runtime of algorithms are stored in ./solutions/runtime.txt
    The number of flows that each algorithm can cover, is saved in ./solutions/Coverage.txt
    The coverage cost of each algorithm is stored in ./solutions/cost_coverage.txt
       
    """

    f = open("./solutions/runtime.txt", "a")

    """
    opt_time_s = time()
    print ('solving opt started')
    optimal_sol(flows, switches)
    opt_time = time() - opt_time_s
    print ('opt time', opt_time)
    f.write(str(opt_time) + " ")
    """

    df_time_s = time()
    print ('solving PMA started')
    pd_sol(flows, switches,capacity)
    #pd_sol(mininet_flows, switches, capacity)
    df_time = time() - df_time_s
    print ('PMA time', df_time)
    f.write(str(df_time)+"\n")


    planck_time_s = time()
    print('solving Planck started')
    planck(flows, switches, capacity, flow_num=flow_num)
    planck_time = time() - planck_time_s
    print('Planck time', df_time)
    f.write(str(planck_time) + "\n")


