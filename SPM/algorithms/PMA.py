import numpy as np

def pd_sol(flows, switches,capacity):
    """
          PMA:
          :param: flows: the list of flows,
          switches: the list of switches,
          capacity: capacity of switches,
          :output:
          Performance parameters of PMA
    """

    """Initializing variables"""
    lambda_i = 0.0
    switch_loads = {}
    for w_id in switches: #setting the load on switches to zero
        switch_loads[w_id] = 0.0
    U = set(flows.values()) #set of uncovered flows
    M = set()
    alpha_f = {}
    beta_w = {}

    flows_sorted = sorted(list(flows.values()), key=lambda x: len(x.ports), reverse=False)
    """ Defining the list showing which flows are mirrored on each switch"""
    mirrored_flows_sitches={x:[] for x in range(1,len(switches)+1)}
    """ Defining the list showing which flows are covered"""
    flows_covered=[]
    """For each uncovered flow find the most cost-efficient switch"""
    for f in flows_sorted:
        if f in U:
            p_hat = None
            p_hat_inc = None
            p_hat_int = None
            for p in f.ports:
                p_inc = max(p.rate if p not in M else 0.0 + switch_loads[p.the_switch.id] - lambda_i, 0)
                p_int = len(p.flows.intersection(U))
                if p_hat is None or p_hat_inc > p_inc / p_int:
                    p_hat = p
                    p_hat_inc = p_inc / p_int
                    p_hat_int = p.flows.intersection(U)
            for f2 in p_hat_int:
                alpha_f[f2.id] = p_hat_inc
            if p_hat not in M:
                M.add(p_hat)
                """Finding the flows that are mirrord on each switch"""
                for f3 in p_hat.flows:
                    mirrored_flows_sitches[p_hat.the_switch.id].append(f3.id)
                switch_loads[p_hat.the_switch.id] += p_hat.rate
            """Find the maximum load switch"""
            lambda_i = max(lambda_i, switch_loads[p_hat.the_switch.id])
            """Update the set of uncovered flows"""
            U = U.difference(p_hat.flows)
    #print('flows on switches:', mirrored_flows_sitches)
    """Update variables alpha and beta"""
    for f_id in flows:
        alpha_f[f_id] = alpha_f[f_id] / (1.0 + max([len(p.flows) for p in flows[f_id].ports]))

    for w_id in switches:
        beta_w[w_id] = max([(sum([alpha_f[f.id] for f in p.flows])/p.rate) if p.rate > 0 else 0.0 for p in switches[w_id].ports])

    #print('primal dual switches',switch_loads)
    """Check whether the mirroring load on each switch is less than the mirroring capacity"""
    sum_load=0
    for switch in switch_loads: 
        if switch_loads[switch] <= capacity:
            sum_load += switch_loads[switch]
            if switch_loads[switch] != 0:
                for index in range(0, len(mirrored_flows_sitches[switch])):
                    if (mirrored_flows_sitches[switch][index] not in flows_covered):
                        flows_covered.append(mirrored_flows_sitches[switch][index])
        elif switch_loads[switch]>capacity:
            sum_load+=capacity
    #print('flows covered:',flows_covered)
    if len(flows_covered)>0:
        sum_load=sum_load/len(flows_covered)
    # else:
    #     sum_load=sum_load

    """Calculating Coverage cost and saving it in file"""
    f_cost_coverage = open("./solutions/cost_coverage.txt", "a")
    f_cost_coverage.write(str(sum_load) + '\n')
    f_cost_coverage.close()

    """calculating the coverage percentage and write it in a file"""
    coverage_percentage = (len(flows_covered) / len(flows_sorted)) * 100
    f_cover = open("./solutions/coverage.txt", "a")
    f_cover.write(str(coverage_percentage) + '\n')
    f_cover.close()
    fw = open('solutions/df', 'w+')
    for p in M:
        fw.write(str(p.the_switch.id) + ' ' + str(p.id) + '\n')
    mininet_write_file('port_config.txt', M)
    #
    fw.write(str(lambda_i) + '\n')
    fw.close()
    f_obj = open("./solutions/obj.txt", "a")
    f_obj.write(str(lambda_i) + '\n')
    f_obj.close()

def mininet_write_file(file_n,result):
    str_n= file_n
    m_file=open(str_n,"a")
    for port in result:
        if str(port.the_switch.id)=='1':
            if str(port.id) == '1':
                m_file.write('s1' + ':' + ' eth1' + '\n')
            if str(port.id) == '2':
                m_file.write('s1' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id)=='2':
            if str(port.id) == '1':
                m_file.write('s2' + ':' + ' eth1' + '\n')
            if str(port.id) == '2':
                m_file.write('s2' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id)=='3':
            if str(port.id) == '1':
                m_file.write('s3' + ':' + ' eth1' + '\n')
            if str(port.id) == '2':
                m_file.write('s3' + ':' + ' eth2' + '\n')
            if str(port.id) == '3':
                m_file.write('s3' + ':' + ' eth3' + '\n')
        if str(port.the_switch.id)=='4':
            if str(port.id) == '1':
                m_file.write('s4' + ':' + ' eth1' + '\n')
            if str(port.id) == '2':
                m_file.write('s4' + ':' + ' eth2' + '\n')
            if str(port.id) == '3':
                m_file.write('s4' + ':' + ' eth3' + '\n')
        if str(port.the_switch.id)=='5':
            if str(port.id) == '1':
                m_file.write('s5' + ':' + ' eth1' + '\n')
            if str(port.id) == '2':
                m_file.write('s5' + ':' + ' eth2' + '\n')
            if str(port.id) == '3':
                m_file.write('s5' + ':' + ' eth3' + '\n')
        if str(port.the_switch.id) == '6':
            if str(port.id) == '1':
                m_file.write('s6' + ':' + ' eth1' + '\n')
            if str(port.id) == '2':
                m_file.write('s6' + ':' + ' eth2' + '\n')
            if str(port.id) == '3':
                m_file.write('s6' + ':' + ' eth3' + '\n')
        if str(port.the_switch.id) == '7':
            if str(port.id) == '1':
                m_file.write('s7' + ':' + ' eth3' + '\n')
            if str(port.id) == '2':
                m_file.write('s7' + ':' + ' eth4' + '\n')
            if str(port.id) == '3':
                m_file.write('s7' + ':' + ' eth1' + '\n')
            if str(port.id) == '4':
                m_file.write('s7' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '8':
            if str(port.id) == '1':
                m_file.write('s8' + ':' + ' eth3' + '\n')
            if str(port.id) == '2':
                m_file.write('s8' + ':' + ' eth4' + '\n')
            if str(port.id) == '3':
                m_file.write('s8' + ':' + ' eth1' + '\n')
            if str(port.id) == '4':
                m_file.write('s8' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '9':
            if str(port.id) == '1':
                m_file.write('s9' + ':' + ' eth3' + '\n')
            if str(port.id) == '2':
                m_file.write('s9' + ':' + ' eth4' + '\n')
            if str(port.id) == '3':
                m_file.write('s9' + ':' + ' eth1' + '\n')
            if str(port.id) == '4':
                m_file.write('s9' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '10':
            if str(port.id) == '1':
                m_file.write('s10' + ':' + ' eth3' + '\n')
            if str(port.id) == '2':
                m_file.write('s10' + ':' + ' eth4' + '\n')
            if str(port.id) == '3':
                m_file.write('s10' + ':' + ' eth1' + '\n')
            if str(port.id) == '4':
                m_file.write('s10' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '11':
            m_file.write('s7' + ':' + ' eth1' + '\n')
        if str(port.the_switch.id) == '12':
            m_file.write('s7' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '13':
            m_file.write('s8' + ':' + ' eth1' + '\n')
        if str(port.the_switch.id) == '14':
            m_file.write('s8' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '15':
            m_file.write('s9' + ':' + ' eth1' + '\n')
        if str(port.the_switch.id) == '16':
            m_file.write('s9' + ':' + ' eth2' + '\n')
        if str(port.the_switch.id) == '17':
            m_file.write('s10' + ':' + ' eth1' + '\n')
        if str(port.the_switch.id) == '18':
            m_file.write('s10' + ':' + ' eth2' + '\n')
