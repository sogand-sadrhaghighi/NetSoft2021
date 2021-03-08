from time import time
from generators import get_topo, get_rand_flows, write_scenario_to_file, read_flows
from algorithms.optimal import optimal_sol
from algorithms.FMA import fms_sol
from algorithms.stroboscope import stroboscope
import optparse

if __name__ == '__main__':
    """Network and flow specifications"""
    parser = optparse.OptionParser()
    """Specify the topology from network folder"""
    parser.add_option('-t', '--topo',
                      action="store", dest="topo_name",
                      help="topo file name in network dir", default="rf1239")
    """ Specifiy the number of flows """
    parser.add_option('-f', '--flow',
                      action="store", dest="flow_num",
                      help="number of flows", default="2")
    """ Specifiy the flow rate range """
    parser.add_option('-l', '--fmin',
                      action="store", dest="min_rate",
                      help="minimum flow rate", default="0.6")
    parser.add_option('-u', '--fmax',
                      action="store", dest="max_rate",
                      help="maximum flow rate", default="2.0")
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
    """Generating the topology"""
    topo, switches = get_topo(topo_name)
    """Reading the flows from a file/Generating flows randomly"""
    if input_flows_file == "":
        flows = get_rand_flows(topo, switches, flow_num, min_rate, max_rate)
    else:
        flows = read_flows(input_flows_file, switches)
    write_scenario_to_file(switches, flows)

    """
        Calling the algorithms
        Runtime of algorithms are stored in ./solutions/runtime.txt
        The value of lambda (maximum switch load) is stored in ./solutions/obj.txt

    """
    f = open("./solutions/runtime.txt", "a")

    # opt_time_s = time()
    # print('solving opt started')
    # optimal_sol(flows, switches)
    # opt_time = time() - opt_time_s
    # print('opt time', time() - opt_time_s)
    # f.write(str(opt_time) + "\n")


    # approx_time_s = time()
    # print ('solving approx started')
    # fms_sol(flows, switches,0.01)
    # approx_time = time() - approx_time_s
    # print ('approx time',approx_time)
    # f.write(str(approx_time)+" ")
    # f.close()

    stroboscope_time_s = time()
    stroboscope(flows,switches,flow_num,topo)
    stroboscope_time =time()-stroboscope_time_s
    print('Stroboscope time', stroboscope_time)
    f.write(str(stroboscope_time) + " ")
    f.close()
