import ast
from collections import defaultdict
import os

#Class to represent a graph 
class Graph: 
    def __init__(self,vertices): 
        self.graph = defaultdict(list) #dictionary containing adjacency List 
        self.V = vertices #No. of vertices 
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 

class Switch:
	def __init__(self, id):
		self.id = id
		self.ports = []
		self.alpha = 0.0
	
	def addPorts(self, ports):
		self.ports = ports
		
class Port:
	def __init__(self, id, dst):
		self.id = id
		self.rate = 0
		self.dst = dst
		self.flows = []

def read_file(filename):
	with open(filename) as file:
		flow_list = []
		flow_id_list = []
		rate = []
		for line in(file.readlines()):
			tmp_line = line.split(':')[0]
			tmp_line = ast.literal_eval(tmp_line)
			flow_list.append([int(f) for f in tmp_line])
			tmp_rate = (line.split(':')[1]).split(',')[1]
			rate.append(int(tmp_rate))
			flow_id_list.append(int((line.split(':')[1]).split(',')[0]))
	return flow_list, rate, flow_id_list		
			
        
def create_topo(graph, flow_list):
	switches = []
	for flow in flow_list:
		flow = flow[1:]
		flow = flow[:-1]
		for f in flow:
			if f not in switches:
				s = Switch(f)
				switches.append(s)
				print(switches)
				#print("Flow: ", f)
				tmp_list = []
				sorted_adjacency = sorted(g.graph[f])
				id = 1
				ports = []
				for v in sorted_adjacency :
					p = Port('eth'+str(id), v)
					id += 1
					ports.append(p)
				s.addPorts(ports)
	return switches

def update_rates(graph, flow_list, switches, rates, flow_id_list):
	rate_index = 0
	id_index = 0
	print(flow_id_list)
	for flow in flow_list:
		flow_id = flow_id_list[id_index]
		flow = flow[1:]
		for i in range(0, len(flow)):
			for switch in switches:
				if switch.id == flow[i]:
					for p in switch.ports:
						if p.dst == flow[i+1]:
							p.rate += rates[rate_index]
							p.flows.append(flow_id_list[id_index])
		rate_index += 1
		id_index += 1

def mirroring(graph, flow_list, switches, flow_id_list):
	id_index = 0
	flows_covered_id = []
	flows_covered = []
	mirroring = set()
	print("Flow list: ", flow_list)
	for flow in flow_list:
		print("Working with flow: ", flow)
		if flow not in flows_covered:
			flow = flow[1:]
			tmp_alpha_values = {}
			for i in range(0, len(flow)):
				for switch in switches:
					if switch.id == flow[i]:
						
						for p in switch.ports:
							if p.dst == flow[i+1]:
								tmp_alpha_values[switch.id] = p.rate+switch.alpha
			min_key = min(tmp_alpha_values, key = tmp_alpha_values.get)
			for i in range(0, len(flow)):
				for switch in switches:
					if switch.id == flow[i] and switch.id == min_key:
						for p in switch.ports:
							if p.dst == flow[i+1]:
								switch.alpha = p.rate+switch.alpha
								for pf in p.flows:
									if pf in flow_id_list:
										index = flow_id_list.index(pf)
										flows_covered_id.append(index)
										flows_covered.append(flow)
								mirroring.add((switch.id, p.id))
								print("Flows covered: ", flows_covered)
			id_index += 1
			
	for elem in mirroring:
		string = "s%d: %s" % (elem[0],str(elem[1]))
		print(string, file=open("port_config.txt", 'a'))						
	for s in switches:
		print("Switch: ", s.id, " with alpha: ", s.alpha)
		for p in s.ports:
			print("Port: ", p.id, " with dst: ", p.dst, " and rate: ", p.rate)

if __name__ == "__main__":
	graph_size = 19
	g = Graph(19)
	g.addEdge(-8, 7)
	g.addEdge(7, -8)
	g.addEdge(-7, 7)
	g.addEdge(7, -7)
	g.addEdge(7, 3)
	g.addEdge(3, 7)
	g.addEdge(7, 4) 
	g.addEdge(4, 7) 
	g.addEdge(3, 1)
	g.addEdge(1, 3)
	g.addEdge(3, 8)
	g.addEdge(8, 3)
	g.addEdge(4, 8)
	g.addEdge(8, 4)
	g.addEdge(4, 2)
	g.addEdge(2, 4)
	g.addEdge(-6, 8)
	g.addEdge(8, -6)
	g.addEdge(-5, 8)
	g.addEdge(8, -5)
	g.addEdge(1, 5)
	g.addEdge(5, 1)
	g.addEdge(2, 6)
	g.addEdge(6, 2)
	g.addEdge(6, 9)
	g.addEdge(9, 6)
	g.addEdge(6, 10)
	g.addEdge(10, 6)
	g.addEdge(5, 9)
	g.addEdge(9, 5)
	g.addEdge(5, 10)
	g.addEdge(10, 5)
	g.addEdge(9, -4)
	g.addEdge(-4, 9)
	g.addEdge(9, -3)
	g.addEdge(-3, 9)
	g.addEdge(10, -2)
	g.addEdge(10, -1)
	g.addEdge(-1, 10)
	g.addEdge(-2, 10)

	if os.path.exists('port_config.txt'):
		os.remove('port_config.txt')
	
	flow_list,rate, flow_id_list = read_file("planckflow.txt")
	print(flow_list)
	print(rate)
	switches = create_topo(g, flow_list)
	update_rates(g, flow_list, switches, rate, flow_id_list)
	mirroring(g, flow_list, switches, flow_id_list)
	
