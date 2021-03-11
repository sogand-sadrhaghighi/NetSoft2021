from collections import defaultdict 
#Python program to print topological sorting of a DAG 
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
  
    # A recursive function used by topologicalSort 
    def topologicalSortUtil(self,v,visited,stack): 
  
        # Mark the current node as visited. 
        visited[v] = True
  
        # Recur for all the vertices adjacent to this vertex 
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack) 
  
        # Push current vertex to stack which stores result 
        stack.insert(0,v) 
  
    # The function to do Topological Sort. It uses recursive  
    # topologicalSortUtil() 
    def topologicalSort(self): 
        # Mark all the vertices as not visited 
        visited = [False]*self.V 
        stack =[] 
  
        # Call the recursive helper function to store Topological 
        # Sort starting from all vertices one by one 
        for i in range(self.V): 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack) 
  
        # Print contents of the stack 
        return stack 

    def orderingUtil(self, list_given):
        list_hosts = [11,12,13,14,15,16,17,18]
        ordered_path = []
        #print(list_given)
        source = next(x for x in list_given if x in list_hosts)
        #print("Source: ", source)
        ordered_path.append(source)
        list_given.remove(source)
        #list_given = [8,4,7,12,13]
       # print(list_given)
        for x in range(0, len(list_given)):
            for v in self.graph[source]:
                #print("Looking at: ", v)
                if v in list_given:
                    list_given.remove(v)
                    ordered_path.append(v)
                    source = v
                    #print("Ordered path is: ", ordered_path, " looking at: ", source)
        if len(list_given) != 0:
            dst = next(x for x in list_given if x in list_hosts)
            list_given.remove(dst)
            ordered_path.append(dst)
        return ordered_path




def read_path(flow_id):
    my_path=[]
    print(flow_id)
    command='grep -Hn %s ./port_mirror/stat_mirror_h2*' %(flow_id)
    result=os.popen(command).readlines()
    for line in result:
        test=line.split(':')[0]
    
        if test.find("_h20") >= 0:
            my_path.append(7)
        elif test.find("_h21") >= 0:
            my_path.append(8)
        elif test.find("_h22") >= 0:
            my_path.append(9)
        elif test.find("_h23") >= 0:
            my_path.append(10)
        elif test.find("_h24") >= 0:
            my_path.append(3)
        elif test.find("_h25") >=0:
            my_path.append(4)
        elif test.find("_h26") >= 0:
            my_path.append(5)
        elif test.find("_h27") >= 0:
            my_path.append(6)
        elif test.find("_h28") >= 0:
            my_path.append(1)
        elif test.find("_h29") >= 0:
            my_path.append(2)
    #    print(my_path)
    return my_path


#if __name__ == "__main__":
def find_route(host1,host2,flow_id):
    if host1=='h1':
        sender_id=11
    elif host1=='h2':
        sender_id=12
    elif host1=='h3':
        sender_id=13
    elif host1=='h4':
        sender_id=14
    elif host1=='h5':
        sender_id=15
    elif host1=='h6':
        sender_id=16
    elif host1=='h7':
        sender_id=17
    elif host1=='h8':
        sender_id=18
    
    if host2=='h1':
        rcv_id=11
    elif host2=='h2':
        rcv_id=12
    elif host2=='h3':
        rcv_id=13
    elif host2=='h4':
        rcv_id=14
    elif host2=='h5':
        rcv_id=15
    elif host2=='h6':
        rcv_id=16
    elif host2=='h7':
        rcv_id=17
    elif host2=='h8':
        rcv_id=18
    
    g= Graph(19) 
    g.addEdge(11, 7)
    g.addEdge(7, 11)
    g.addEdge(12, 7)
    g.addEdge(7, 12)
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
    g.addEdge(13, 8)
    g.addEdge(8, 13)
    g.addEdge(14, 8)
    g.addEdge(8, 14)
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
    g.addEdge(9, 15)
    g.addEdge(15, 9)
    g.addEdge(9, 16)
    g.addEdge(16, 9)
    g.addEdge(10, 17)
    g.addEdge(10, 18)
    g.addEdge(18, 10)
    g.addEdge(17, 10)

    
    #print ("Following is a Topological Sort of the given graph")
    
    #topo_list = g.topologicalSort() 
    #print("Topology sorted: ",topo_list)
    # Get the list by reading from stat files
    list_given=read_path(flow_id)
    #print(list_given)
    list_given.append(sender_id)
    list_given.append(rcv_id)
    #print("After: ", list_given)
    #list_given = [10,6,2,4,7,17,11]
    return g.orderingUtil(list_given)
    #orderedList = sorted(list_given, key=lambda x: topo_list.index(x))

    #return []
    

#if __name__=="__main__":
#    print(find_route('h2','h3',str(31)))
