
from itertools import combinations

def stroboscope( flows, switches, flow_num,topo):
    """
        stroboscope:
        :param: flows: the list of flows,
        switches: the list of switches,
        flow_num: total number of flows,
        topo: topology,
        :output:
        Performance parameters of Optimal
    """

    """ Shows the mirroring load on each switch"""
    switch_mirror_load= [0 for i in range(1, len(switches)+2)]
    flow_index=1
    while flow_index<=flow_num:
        mirroring_locations = []
        """Find the default shortest path for a flow"""
        default_path=[switch.id for switch in flows[flow_index].switches]
        #print('default path:', default_path)
        # for port in flows[flow_index].ports:
        #     print('path: ',port.dst_switch.id)
        TTL = len(default_path)-1
        visited = [False for i in range(1, len(switches)+2)]
        path = []
        path_length = 0
        """Find if there is any other possible path for a flow"""
        other_path = False
        other_path = (printAllPathsUtil(default_path[0], default_path[-1], visited, path, switches, path_length, TTL,other_path,default_path,topo))
        max_concat=default_path
        while other_path==True:
            concat = concatenations(max_concat)
            max_concat = max(concat, key = lambda i: len(i)) # Finding the maximum subpath
            TTL = len(max_concat) - 1
            visited = [False for i in range(1, len(switches) + 2)]
            path = []
            path_length = 0
            other_path = False
            other_path = (
                printAllPathsUtil(max_concat[0], max_concat[-1], visited, path, switches, path_length, TTL, other_path,
                                  max_concat,topo))

        """"Find mirroring locations based on possible branches in the paths"""
        mirroring_locations.append(max_concat[0])
        mirroring_locations.append(max_concat[-1])
        difference_path = [x for x in default_path if x not in max_concat]
        if len(difference_path) == 1:
            mirroring_locations.append(difference_path[0])
        while len(difference_path) > 1:
            max_concat = find_mirroring_locations(difference_path, switches,topo)
            mirroring_locations.append(max_concat[0])
            mirroring_locations.append(max_concat[-1])
            difference_path = [x for x in difference_path if x not in max_concat]
            if len(difference_path) == 1:
                mirroring_locations.append(difference_path[0])
        #print('mirroring locations: ', mirroring_locations

        """Find the mirroring load based on mirroring locations"""
        temp = mirror_switch(mirroring_locations, flows[flow_index].rate, switch_mirror_load)
        flow_index += 1

    """Find the maximum mirroring load and save the performance parameters in a file"""
    lambda_i= max(temp)
    print(lambda_i)
    f_obj = open("./solutions/obj.txt", "a")
    f_obj.write(str(lambda_i) + '\n')
    f_obj.close()








def printAllPathsUtil(u, d, visited, path, switches, path_length, TTL,other_path, default_path,topo):
    '''
        A recursive function to print all paths from 'u' to 'd'.
        visited[] keeps track of vertices in current path.
        path[] stores actual vertices and path_index is current
        index in path[]
    '''
    # Mark the current node as visited and store in path
    # print("This is u: ", u)
    # print("This is d: ", d)
    # print("This is TTL:", TTL)
    # print("This is path length:", path_length)

    visited[u] = True
    path.append(u)
    # print("path_length:", path_length)
    # If current vertex is same as destination, then print
    # current path[]
    if path_length <= TTL:
        if u == d:
            if path_length == TTL:
                if path != default_path:
                    other_path = True
                    # print(path)
                    return other_path
            path_length = 0
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex

            for i in topo[u].keys():
                # print('u:', u)
                # print('i', i)
                if not visited[i]:
                    # path_length += 1
                    if other_path == True:
                        break
                    else:
                        other_path = printAllPathsUtil(i, d, visited, path, switches, path_length+1, TTL,other_path,default_path,topo)

                # Remove current vertex from path[] and mark it as unvisited

    path.pop()
    visited[u] = False
    return other_path

    # print(output_path)



# print all the combinations of a path

def concatenations(path):
    path_tmp = [str(i) for i in path]
    longest_concat = [path_tmp[x:y] for x, y in combinations(
            range(len(path_tmp) + 1), r = 2)]
    filtered_concat = [concat for concat in longest_concat if len(concat) >= 2]

    int_outer_set=[]
    for outer_set in filtered_concat:
        int_inner_set = []
        for inner_set in outer_set:
            int_inner_set.append(int(inner_set))
        if int_inner_set != path:
            int_outer_set.append(int_inner_set)
    return int_outer_set

def find_mirroring_locations(diff_path,switches,topo):
    # concat = concatenations(max_concat)
    # max_concat= max(concat, key = lambda i: len(i)) # Finding the maximum subpath
    TTL = len(diff_path) - 1
    visited = [False for i in range(1, len(switches) + 2)]
    path = []
    path_length = 0
    other_path = False
    other_path = (printAllPathsUtil(diff_path[0], diff_path[-1], visited, path, switches, path_length, TTL, other_path, diff_path, topo))
    # print('find_mirroring_locations',other_path)
    max_concat = diff_path
    while other_path:
        diff_path = concatenations(max_concat)
        max_concat = max(diff_path, key=lambda i: len(i))  # Finding the maximum subpath
        TTL = len(max_concat) - 1
        visited = [False for i in range(1, len(switches) + 2)]
        path = []
        path_length = 0
        other_path = False
        other_path = (
            printAllPathsUtil(max_concat[0], max_concat[-1], visited, path, switches, path_length, TTL, other_path,
                              max_concat,topo))
        print(other_path)
    return max_concat

def mirror_switch(switch_list,flow_rate,switch_mirror_load):
    for i in switch_list:
        switch_mirror_load[i]+=flow_rate
    return switch_mirror_load
