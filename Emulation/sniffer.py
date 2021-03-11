from socket import * 
from struct import unpack 
import sys 
import os
import time

if __name__ == "__main__":
    TARGET = sys.argv[1]
    #DESTINATION = "10.0.0.1"
    INTERFACE = sys.argv[2]
    FILENAME = sys.argv[3]
    #print(FILENAME)
    sock = socket(AF_PACKET, SOCK_DGRAM, 0x0800)
    sock.bind((INTERFACE, 0x0800))
    zrr_pck_counter = 1
    pck_counter=1
    sock.settimeout(20)#50
    #print("", file=open(FILENAME,"a"))
    #print(str(TARGET)+"\n",file=open(FILENAME,"a"))
    stat_dic={}
    packet_dic={}# list of collected packets in each flow
    identifier_list=[]
    #if os.path.exists(FILENAME):
    #    os.remove(FILENAME)
    while True:
        try:
            data = sock.recvfrom(2000, 0)[0]
            ip = inet_ntop(AF_INET, data[16:20])
            ip2 = inet_ntop(AF_INET, data[12:16])
            #print("SRC: " + ip2, file=open(FILENAME,"a"))
            #print(str(ip2) == TARGET, file=open(FILENAME,"a"))
            #print(len(data), file=open(FILENAME,"a"))
            if str(ip2) == TARGET:# and str(ip2) == DESTINATION:
                splt_data=str(data).split("-")[1]
                counter_str=str(data).split("-")[2]
                #print(str(counter_str), file=open(FILENAME,"a"))
                try:
                    if int(splt_data) in packet_dic:
                        packet_dic[int(splt_data)].append(int(counter_str))
                    else:
                        packet_dic[int(splt_data)]=[int(counter_str)]
                    x = int(splt_data)
                    if len(data) == 1278:
                        if str(data).find("Zorro")>=0:
                            if int(splt_data) not in identifier_list:
                                identifier_list.append(int(splt_data))
                                if int(splt_data) in stat_dic:
                                    zrr_pck_counter = stat_dic[int(splt_data)][0] + 1
                                    pck_counter  = stat_dic[int(splt_data)][1] + 1
                                    d1={int(splt_data):(zrr_pck_counter,pck_counter)}
                                    stat_dic.update(d1)
                                else:
                                    zrr_pck_counter = 1
                                    pck_counter = 1
                                    stat_dic[int(splt_data)]=(zrr_pck_counter,pck_counter)
                        else:
                            if int(splt_data) in stat_dic:
                                zrr_pck_counter = stat_dic[int(splt_data)][0]
                                pck_counter  = stat_dic[int(splt_data)][1] + 1
                                d1={int(splt_data):(zrr_pck_counter,pck_counter)}
                                stat_dic.update(d1)
                            else:
                                zrr_pck_counter = 0
                                pck_counter = 1
                                stat_dic[int(splt_data)]=(zrr_pck_counter,pck_counter)
                        splt_data = ""
                        print(stat_dic)
                except ValueError:
                    splt_data = ""
                #write_str = "Zorro packets sniffed from host\t%s:\t%d" % (ip,zrr_pck_counter)
                #print(write_str, file=open(FILENAME,"a"))
            #write_str1="Total packets sniffed from host\t%s:\t%d" % (ip,pck_counter)
            #print(write_str1,file=open(FILENAME,"a"))
            #print(data, file=open(FILENAME, "a"))
        except OSError:
            if bool(stat_dic):
                #print(stat_dic, file=open(FILENAME,"a"))
                for key in stat_dic:
                    write_str = "Host:\t%s\tTotal:\t%d\tZorror:\t%d\tid:\t%s\tcounter\t%s" % (key,stat_dic[key][1],stat_dic[key][0],key, set(packet_dic[key]))
                    print(write_str, file=open(FILENAME,"a"))
               # for element in identifier_list:
               #     print(str(element), flush=True, file=open(FILENAME,"a"))
            else:
                print("Dictionary was empty", file=open(FILENAME,"a"))
            #write_str1="Total packets sniffed from host\t%s:\t%d" % (ip,pck_counter)
            #print(write_str1,file=open(FILENAME,"a"))
            sys.exit(0)
        
