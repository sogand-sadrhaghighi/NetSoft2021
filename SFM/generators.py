import numpy as np
import networkx as nx

class Flow:
    """
        Generate flows:
        Each flow has a unique ID, rate,
        and the ports that it passed on
        each switch (based on routing)
    """
    def __init__(self, id, rate):
        self.id = id
        self.rate = rate
        self.switches = set()

    def add_switch(self, switch):
        self.switches.add(switch)


class Switch:
    """
        Each switch has an ID and
        ID of ports belonging to it
    """
    def __init__(self, id):
        self.id = id
        self.flows = set()

    def add_flow(self, f):
        self.flows.add(f)

    def get_sorted_flows(self):
        return sorted(self.flows, key=lambda f: f.rate, reverse=True)

    def get_total_traffic(self):
        return sum([f.rate for f in self.flows])


def get_topo(topo_name):
    """
        :param topo_name: Get the name of a topology file
        :return: generates the topology graph,
        the list of switches, a list of links
    """

    """Initializing variable"""
    switches = dict()
    topo = nx.Graph()
    topo_file = open('network/' + topo_name, 'r')

    """The first line of each topology file, contains the ID of all switches"""
    switch_num = topo_file.readline()
    switch_ids = range(1, int(switch_num) + 1)
    """Generating the switches as nodes of the graph/ generating the links"""
    for w_id in switch_ids:
        topo.add_node(w_id)
        switches[w_id] = Switch(w_id)
    for l in topo_file:
        if len(l) <= 1:
            continue
        if l[-1] == '\n':
            link_info = l[:-1].split(' ')
        else:
            link_info = l.split(' ')
        topo.add_edge(int(link_info[0]), int(link_info[1]))
    return topo, switches


def get_rand_flows(topo, switches, flow_num, min_rate, max_rate):
    """
        generating random flows
        :param topo: Get the topology,
        switches: list of switches,
        flow_num: number of flows,
        min_rate: the lower bound for flow rates
        max_rate: the upper bound for flow rates
        :return: flows: generate random flows
    """
    flows = dict()
    for f_id in range(1, flow_num + 1):
        f = Flow(f_id, np.random.uniform(min_rate, max_rate))
        flows[f_id] = f
        new_array=[]
        for key in switches.keys():
            new_array.append(key)
        sws = np.random.choice(new_array, 2, replace=False)
        # sws = np.random.choice(switches.keys(), 2, replace=False)
        w_path = nx.shortest_path(topo, sws[0], sws[1])
        for w_path_id in w_path:
            switches[w_path_id].add_flow(f)
            f.add_switch(switches[w_path_id])
    return flows


def read_flows(file_name, switches):
    """
        Reading flows from a file, instead of generating random flows
        :param topo_name: Get the name of a file,
        the list of switches
        :return: Set of read flows
    """
    flows_file = open('network/'+file_name, 'r')
    flows = dict()
    for line in flows_file:
        if len(line) <= 1:
            continue
        if line[-1] == '\in':
            line = line[:-1]
        flow_info = line.split(' ')
        f_id = int(flow_info[0])
        f_rate = float(flow_info[1])
        f = Flow(f_id, f_rate)
        flows[f_id] = f
        for w_id in flow_info[2:]:
            w_id = int(w_id)
            switches[w_id].add_flow(f)
            f.add_switch(switches[w_id])
    return flows


def write_scenario_to_file(switches, flows):
    """
        Write the scenario to the file
        :param topo_name: Get the list of switches
        and the set of generated flows
        :return: Write the scenario in the file
    """
    switch_file = open('network/switches', 'w+')
    for w in switches.values():
        fs = str(w.id)
        for f in w.flows:
            fs = fs + ' ' + str(f.id)
        fs = fs + '\n'
        switch_file.write(fs)
    switch_file.close()
    flow_file = open('network/flows', 'w+')
    for f_id in flows:
        fs = str(f_id) + ' ' + str(flows[f_id].rate)
        for w in flows[f_id].switches:
            fs = fs + ' ' + str(w.id)
        fs = fs + '\n'
        flow_file.write(fs)
    flow_file.close()
