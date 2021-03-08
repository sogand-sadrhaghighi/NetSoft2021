def read_file(file_name):
    f = open(file_name, "r")
    lines=f.readlines()
    path=[]
    for line in lines:
        path_str=(line.split('[')[1]).split(']')[0]
        id= ((line.split('[')[1]).split(']')[1]).split(',')[0]
        flow_rate = ((line.split('[')[1]).split(']')[1]).split(',')[1]
        path_str_splt=path_str.split(',')
        for p in path_str_splt:
            path.append(int(p))
    return path,id, flow_rate

