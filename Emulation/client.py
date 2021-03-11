import socket
import sys
import random

def sender(UDP_IP,FILENAME,IDENTIFIER,COUNTER):
    print(UDP_IP)
    print(FILENAME)
    UDP_PORT = 23
    zrr_pkt_counter=0
    pkt_counter=0
    #print(str(COUNTER),file=open("test.txt","a"))
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    i=random.uniform(0,1)
    pkt_counter+=1
    #if int(COUNTER)<=2 and i<=1:
    if int(COUNTER)==10:
        zrr_pkt_counter+=1
        #print("here",file=open("test.txt","a"))
        write_str= "Zorro\t%d" %zrr_pkt_counter
        print(write_str,file=open(FILENAME+".txt","a"))
        txt="Zorro-"+str(IDENTIFIER)+"-"+str(COUNTER)+"-"
        message=txt.ljust(1250,"o")
    else:
        write_str= "Not_Z\t%d" % pkt_counter
        print(write_str,file=open(FILENAME+".txt","a"))
        txt="Garbage-"+str(IDENTIFIER)+"-"+str(COUNTER)+"-"
        message=txt.ljust(1250,"o")
    message=bytes(message, 'utf-8')

    sock.sendto(message, (UDP_IP,UDP_PORT))
    sock.close()
#    write_str="Dst:\t%s\tTotal:%d\tZorro:%d" %(UDP_IP,pkt_counter,zrr_pkt_counter) 
   # print('###',file=open(FILENAME,"a"))
    sys.exit(0)

if __name__=='__main__':
    print('client')
    UDP_IP = sys.argv[1]
    FILENAME = sys.argv[2]
    IDENTIFIER=sys.argv[3]
    COUNTER=sys.argv[4]
    sender(UDP_IP,FILENAME,IDENTIFIER,COUNTER)
