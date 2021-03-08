import numpy as np
def planck(flows,switches,capacity, flow_num):
    """
        Planck:
        :param: flows: the list of flows,
        switches: the list of switches,
        capacity: the mirroring capacity of switches,
        flow-num: the number of flows,
        :output:
        Performance parameters of Planck
    """

    """Initializing variables"""
    flow_index=1
    """List of flows passing throug a switch"""
    switch_mirroring = {x:[] for x in range(1,len(switches)+1)}
    """Dictionary of mirroring load on each switch"""
    mirror_load = {x:0 for x in range(1,len(switches)+1)}
    flows_covered = []

    """Find the flows passing through each switch"""
    while flow_index<=flow_num:
        flow_path= [port.the_switch.id for port in flows[flow_index].ports]
        for switch in flow_path:
            switch_mirroring[switch].append(flow_index)
        flow_index+=1

    """Find the mirroring load on each switch"""
    for switch in switch_mirroring:
        load=0
        if len(switch_mirroring[switch])!= 0:
            for index in range(0,len(switch_mirroring[switch])):
                load+= flows[switch_mirroring[switch][index]].rate
        mirror_load[switch] =load

    """Find the objective value (the maximum mirroring load among switches) and save the result in a file"""
    obj = max([i for i in mirror_load.values()])
    f_obj = open("./solutions/obj.txt", "a")
    f_obj.write(str(obj) + '\n')
    f_obj.close()
    sum_load=0

    """Find the mirroring load on switches if there is a capacity constraint on each switch"""
    for switch in mirror_load:
        if mirror_load[switch]<=capacity:
            sum_load += mirror_load[switch]
            if len(switch_mirroring[switch]) != 0:
                for index in range(0, len(switch_mirroring[switch])):
                    if(switch_mirroring[switch][index] not in flows_covered):
                        flows_covered.append(switch_mirroring[switch][index])
        elif mirror_load[switch]>capacity:
            sum_load+=capacity

    if len(flows_covered)!=0:
        sum_load=sum_load/len(flows_covered)
    # else:
    #     sum_load =sum_load

    """Find the coverage cost and coverage of Planck and save them in files"""
    f_cost_coverage = open("./solutions/cost_coverage.txt", "a")
    f_cost_coverage.write(str(sum_load) + '\n')
    f_cost_coverage.close()
    #print('planck flows covered:',flows_covered)
    coverage_percentage= (len(flows_covered)/flow_num) *100
    f_coverage = open("./solutions/coverage.txt", "a")
    f_coverage.write(str(coverage_percentage) + '\n')
    f_coverage.close()



