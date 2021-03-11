import glob
import os


def write_flow():
    stat_dic={}
    zorro_counter=0#global zorro
    total_counter=0#global total
    if os.path.exists('gurobi.txt'):
        os.remove('gurobi.txt')
    for f in glob.glob("port_mirror/client/*.txt"):
        tmp=(f.split("/")[-1]).split(".txt")[0]
        sender=tmp.split("-")[0]
        receiver=tmp.split("-")[1]
        command='wc -l \"%s\" | awk \'{print $0/3}\'' % f
        p=os.popen(command)
        number_lines=p.read()
        zrr_counter,counter=Lastlines(f, int(number_lines))
        total=zrr_counter+counter
       # print(zrr_counter)
        print(str(sender)+"-"+str(receiver)+'\t'+"Zorro:"+str(zrr_counter)+'\t'+"Total:"+str(total))
        size=total*1250
        print("("+str(sender)+","+str(receiver)+"):"+str(size), file=open("gurobi.txt","a"))
        #stat_dic[(sender,receiver)]=(zrr_counter,total)
        zorro_counter+=zrr_counter
        total_counter+=total
    print("Sent"+'\t'+"Total:",total_counter,'\t',"Zorro:",zorro_counter)
        


    """
    for f in glob.glob("port_mirror/client/*_zorro.txt"):
        tmp=(f.split("/")[-1]).split(".txt")[0]
        sender=tmp.split("-")[0]
        receiver=tmp.split("-")[1]
        size= 10*1250
        print("("+str(sender)+","+str(receiver)+"):"+str(size), file=open("gurobi.txt","w"))
   """         
def Lastlines(fname,number_lines):
    zrr_counter=0
    counter=0
    with open(fname) as file:
        for line in(file.readlines() [-number_lines:]):
            tmp=line.split('\t')[0]
            if tmp.find("Zorro")>=0:
                zrr_counter+=1
            else:
                counter+=1
    return zrr_counter,counter

def sniffer_stat():
    zrr_counter=0
    total_counter=0
    id_list=[]
    sent_packet=0# Total number of packet sent
    sniffed_packet={}#total number of packet sniffedi
    total_sniffed=0
    for f in glob.glob("port_mirror/*.txt"):
        with open(f) as file:
            l1=file.readline()
            for line in (file.readlines()):
                if line.find("Dictionary")==-1:
                    total=line.split('\t')[3]
                    zorro=line.split('\t')[5]
                    identifier=line.split('\t')[7]
                    counter_list=((line.split('\t')[9]).split('{')[1]).split('}')[0]
                    counter_list_int=[int(s) for s in counter_list.split(',')]
                    #print("counter: ",counter_list_int)
                    search_key=int(identifier)
                    if search_key in sniffed_packet.keys():
                        if sniffed_packet[int(identifier)]<len(counter_list_int):
                            sniffed_packet[int(identifier)]=len(counter_list_int)
                    else:
                        sniffed_packet[int(identifier)]=len(counter_list_int)
                    #print("sent packet: ",total_packet_sent,"sniffed packet: ",len(counter_list_int))
                    if int(identifier) not in id_list and int(zorro) > 0:
                        id_list.append(int(identifier))
                        zrr_counter+=int(zorro)
                    total_counter+=int(total)
    for in_file in glob.glob("sent_perflow/*.txt"):
        with open(in_file) as file1:
            total_packet_sent=int(file1.readline())
            sent_packet+=total_packet_sent
    for key in sniffed_packet:
        total_sniffed=total_sniffed+sniffed_packet[key]


    print("Sniffed"+'\t'+"Total:",total_counter,'\t',"Zorro:",zrr_counter)
    print("Sniffed packet",total_sniffed,'\t'+"Sent Packet:",sent_packet)
                    
if __name__=="__main__":
    write_flow()
    sniffer_stat()
