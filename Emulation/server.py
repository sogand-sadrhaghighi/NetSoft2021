import socket
import sys
import os
import time

def server(argv):
    UDP_IP = argv[0]
    path=argv[1]
    UDP_PORT = 23
    start_time=time.time()
    time_out=10
    print("Binding")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print("Listening")
    counter=0
    zorro_counter=0
    sock.settimeout(10)
    if os.path.exists(path):
        os.remove(path)
    while True:
        data, addr = sock.recvfrom(1024)
        counter+=1
        print(str(data))
        if str(data).find("Zorro")>0:
            zorro_counter+=1
            print(zorro_counter)
           # return
        print("zorro packets found: "+str(zorro_counter),file=open(path,"a"))
        print("total packets: "+ str(counter),file=open(path,"a"))
        #print("Current time is: " + str(time.time()))
        #print("Start time is: " + str(start_time))
        if not data:
            break
        if time.time()-start_time>time_out:
            socket.close()
            sys.exit(0)
if __name__=='__main__':
    server(sys.argv[1:])
