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
        self.ports = []

    def add_port(self, port):
        self.ports.append(port)


class Port:
    """
        Each port has a set of flows that pass through it,
        the total rate of flows traversing it,
        the ID of the switch it belongs to,
        the ID of the switch it connects to
    """
    def __init__(self, id, the_switch, dst_switch):
        self.id = id
        self.flows = set()
        self.rate = 0.0
        self.flow_num = 0
        self.dst_switch = dst_switch
        self.the_switch = the_switch

    def calc_rate(self):
        self.rate = 0.0
        for f in self.flows:
            self.rate += f.rate

    def calc_flow_num(self):
        self.flow_num = 0
        for _ in self.flows:
            self.flow_num += 1


class Switch:
    """
        Each switch has an ID and
        ID of ports belonging to it
    """
    def __init__(self, id):
        self.id = id
        self.ports = list()

    def get_total_rate(self):
        return sum([p.rate for p in self.ports])

    def get_port_by_id(self, port_id):
        for port in self.ports:
            if port.id == port_id:
                return port

    def get_port_by_next_hop(self, next_hop):
        for port in self.ports:
            if port.dst_switch == next_hop:
                return port


def get_topo(topo_name):
    """
    :param topo_name: Get the name of a topology file
    :return: generates the topology graph,
    the list of switches, a list of links
    """

    """Initializing variable"""
    switches = dict()
    topo = nx.DiGraph()
    topo_file = open('network/' + topo_name, 'r')

    """The first line of each topology file, contains the ID of all switches"""
    switch_num = topo_file.readline()
    switch_ids = range(1, int(switch_num) + 1)
    for w_id in switch_ids:
        topo.add_node(w_id)
        switches[w_id] = Switch(w_id)

    """Generating the end hosts"""
    edges_str = topo_file.readline()
    while len(edges_str) > 0 and edges_str[-1] in [' ', '\n', '\r', '\t']:
        edges_str = edges_str[:-1]
    if len(edges_str) > 0:
        edges_id = [int(h_id) for h_id in edges_str.split(' ')]
        print("edge id:",edges_id)
    else:
        edges_id = []
    for l in topo_file:
        if len(l) <= 1:
            continue
        if l[-1] == '\n':
            link_info = l[:-1].split(' ')
        else:
            link_info = l.split(' ')

        """Finding the edges in the topology graph"""
        topo.add_edge(int(link_info[0]), int(link_info[1]), weight=0.0)
        topo.add_edge(int(link_info[1]), int(link_info[0]), weight=0.0)

        """Finding the port IDs involved in each link"""
        p0 = Port(len(switches[int(link_info[0])].ports)+1, switches[int(link_info[0])], switches[int(link_info[1])])
        p1 = Port(len(switches[int(link_info[1])].ports)+1, switches[int(link_info[1])], switches[int(link_info[0])])

        switches[int(link_info[0])].ports.append(p0)
        switches[int(link_info[1])].ports.append(p1)

    return topo, switches, edges_id


def get_rand_flows(topo, switches, endpoints, flow_num, min_rate, max_rate):
    flows = dict()
    f_id = 1
    while f_id <= flow_num:
        if endpoints is None or len(endpoints) == 0:
            sws = np.random.choice(list(switches.keys()), 2, replace=False)
        else:
            sws = np.random.choice(endpoints, 2, replace=False)
        w_path = nx.shortest_path(topo, sws[0], sws[1], weight='weight')
        # if len(w_path) <= 4:
        #     continue
        f = Flow(f_id, np.random.uniform(min_rate, max_rate))
        flows[f_id] = f
        f_id += 1
        for l in range(len(w_path)-1):
            switches[w_path[l]].get_port_by_next_hop(switches[w_path[l+1]]).flows.add(f)
            f.add_port(switches[w_path[l]].get_port_by_next_hop(switches[w_path[l+1]]))
            switches[w_path[l]].get_port_by_next_hop(switches[w_path[l + 1]]).calc_rate()
            switches[w_path[l]].get_port_by_next_hop(switches[w_path[l + 1]]).calc_flow_num()
            topo[w_path[l]][w_path[l+1]]['weight'] += f.rate
    return flows

def mininet_read_flows(file_name,switches,topo):
    """
    :param file_name: Get the name of a file,
    switches: the list of switches and,
    topo: the topology,
    :return: generates the topology graph,
    Using Mininet generated flows
    """
    file_r = open(file_name, "r")
    lines = file_r.readlines()
    flows = dict()
    id=1
    for line in lines:
        path = []
        print(line)
        path_str = (line.split('[')[1]).split(']')[0]
        flow_rate = ((line.split('[')[1]).split(']')[1]).split(',')[1]
        flow_rate=float(flow_rate)
        path_str_splt = path_str.split(',')
        for p in path_str_splt:
            path.append(int(p))
        f=Flow(id,flow_rate)
        flows[id]=f
        for l in range(len(path)-1):
            switches[path[l]].get_port_by_next_hop(switches[path[l+1]]).flows.add(f)
            f.add_port(switches[path[l]].get_port_by_next_hop(switches[path[l+1]]))
            switches[path[l]].get_port_by_next_hop(switches[path[l + 1]]).calc_rate()
            switches[path[l]].get_port_by_next_hop(switches[path[l + 1]]).calc_flow_num()
            topo[path[l]][path[l+1]]['weight'] += f.rate
        id+=1
    return flows

def read_flows(file_name, switches):
    """
       Reading flows from a file, instead of generating random flows
       :param topo_name: Get the name of a file,
       the list of switches
       :return: Set of read flows
    """
    flows_file = open('./network/'+file_name, 'r')
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
        for i in range(int(len(flow_info[2:])/2)):
            w_id = int(flow_info[2+2*i])
            p_id = int(flow_info[2+2*i+1])
            switches[w_id].get_port_by_id(p_id).flows.add(f)
            f.add_port(switches[w_id].get_port_by_id(p_id))
            switches[w_id].get_port_by_id(p_id).calc_rate()
            switches[w_id].get_port_by_id(p_id).calc_flow_num()
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
        for p in w.ports:
            fs = str(w.id) + ' ' + str(p.id) + ' ' + str(p.rate)
            for f in p.flows:
                fs = fs + ' ' + str(f.id)
            fs = fs + '\n'
            switch_file.write(fs)
    switch_file.close()

    flow_file = open('network/flows', 'w+')
    for f_id in flows:
        fs = str(f_id) + ' ' + str(flows[f_id].rate)
        for p in flows[f_id].ports:
            fs = fs + ' ' + str(p.the_switch.id) + ' ' + str(p.id)
        fs = fs + '\n'
        flow_file.write(fs)
    flow_file.close()

def write_fat_tree_to_file(pod_num, file_name):
    """
        Generate a x-pod fattree topology
        :param topo_name: Get the number of pods in the fattree
        :return: Write the generated fattree in the file
    """

    """Initializing variables"""
    fw = open(file_name, 'w')
    sw_counter = 1
    links = []
    servers = {}
    edges = {}

    """Find the links in the fattree"""
    for p in range(pod_num):
        for e in range(pod_num/2):
            edges[(p,e)] = sw_counter
            sw_counter += 1


    """Find the list of aggregate switches"""
    aggs = {}
    for p in range(pod_num):
        for a in range(pod_num/2):
            aggs[(p,a)] = sw_counter
            sw_counter += 1

    """Find the list of core switches"""
    cores = {}
    for c1 in range(pod_num / 2):
        for c2 in range(pod_num / 2):
            cores[(c1, c2)] = sw_counter
            sw_counter += 1

    """Find the list of servers"""
    for s in servers:
        p = s[0]
        e = s[1]
        links.append((servers[s], edges[(p,e)]))
    for e in edges:
        pe = e[0]
        for a in aggs:
            pa = a[0]
            if pe == pa:
                links.append((edges[e],aggs[a]))
    for c in cores:
        for p in range(pod_num):
            a = (p, c[1])
            links.append((cores[c], aggs[a]))

    """Write the total fattree in the file"""
    fw.write(str(sw_counter-1) + '\n')
    for e in edges:
        fw.write(str(edges[e]) + ' ')
    fw.write('\n')
    for l in links:
        fw.write('%d %d\n' %(l[0], l[1]))
    fw.close()
