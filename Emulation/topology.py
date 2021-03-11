
from mininet.topo import Topo
from mininet.node import Controller, RemoteController
from mininet.node import UserSwitch, Host, Node, OVSKernelSwitch
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import threading
import pyshark
from scapy.all import *
import time
import random
from find_routing import find_route
def FatTree():
	net = Mininet (controller= RemoteController)
	net.addController ('c0',controller=RemoteController,ip="127.0.0.1", port=6633)
	
	s1=net.addSwitch('s1',protocols='OpenFlow13')
	s2=net.addSwitch('s2',protocols='OpenFlow13')
	s3=net.addSwitch('s3',protocols='OpenFlow13')
	s4=net.addSwitch('s4',protocols='OpenFlow13')
	s5=net.addSwitch('s5',protocols='OpenFlow13')
	s6=net.addSwitch('s6',protocols='OpenFlow13')
	s7=net.addSwitch('s7',protocols='OpenFlow13')
	s8=net.addSwitch('s8',protocols='OpenFlow13')
	s9=net.addSwitch('s9',protocols='OpenFlow13')
	s10=net.addSwitch('s10',protocols='OpenFlow13')

	s21=net.addSwitch('s21',protocols='OpenFlow13')
		
	h1=net.addHost('h1',ip="10.0.0.1")
	h2=net.addHost('h2',ip="10.0.0.2")
	h3=net.addHost('h3',ip="10.0.0.3")
	h4=net.addHost('h4',ip="10.0.0.4")
	h5=net.addHost('h5',ip="10.0.0.5")
	h6=net.addHost('h6',ip="10.0.0.6")
	h7=net.addHost('h7',ip="10.0.0.7")
	h8=net.addHost('h8',ip="10.0.0.8")
	

	h20=net.addHost('h20',ip="10.0.0.20")
	h21=net.addHost('h21',ip="10.0.0.21")
	h22=net.addHost('h22',ip="10.0.0.22")
	h23=net.addHost('h23',ip="10.0.0.23")
	h24=net.addHost('h24',ip="10.0.0.24")
	h25=net.addHost('h25',ip="10.0.0.25")
	h26=net.addHost('h26',ip="10.0.0.26")
	h27=net.addHost('h27',ip="10.0.0.27")
	h28=net.addHost('h28',ip="10.0.0.28")
	h29=net.addHost('h29',ip="10.0.0.29")
		
	net.addLink(h1,s7)
	net.addLink(h2,s7)
	net.addLink(h3,s8)
	net.addLink(h4,s8)
	net.addLink(h5,s9)
	net.addLink(h6,s9)
	net.addLink(h7,s10)
	net.addLink(h8,s10)

	net.addLink(s1,s3)
	net.addLink(s1,s5)
	net.addLink(s2,s4)
	net.addLink(s2,s6)
	net.addLink(s3,s7)
	net.addLink(s3,s8)
	net.addLink(s4,s7)
	net.addLink(s4,s8)

	
	net.addLink(s5,s9)
	net.addLink(s5,s10)
	net.addLink(s6,s9)
	net.addLink(s6,s10)
	
	
	net.addLink(s7,h20,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s8,h21,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s9,h22,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s10,h23,cls=TCLink,bw=10,max_queue_size=1)
	
	net.addLink(s3,h24,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s4,h25,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s5,h26,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s6,h27,cls=TCLink,bw=10,max_queue_size=1)#,bw=100,max_queue_size=1
	
	net.addLink(s1,h28,cls=TCLink,bw=10,max_queue_size=1)
	net.addLink(s2,h29,cls=TCLink,bw=10,max_queue_size=1)
	
	net.start()
	
	#_________________Planck:Mirroring all ports_________________________________
	#Planck works by enabling port mirroring on all ports and assign a port to mirror on it
	
	'''
	s7.cmd('ovs-vsctl del-port s7-eth5')
	s7.cmd('ovs-vsctl add-port s7 s7-eth5 -- --id=@p get port s7-eth5 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s7 mirrors=@m')
	
	s8.cmd('ovs-vsctl del-port s8-eth5')
	s8.cmd('ovs-vsctl add-port s8 s8-eth5 -- --id=@p get port s8-eth5 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s8 mirrors=@m')
	
	s9.cmd('ovs-vsctl del-port s9-eth5')
	s9.cmd('ovs-vsctl add-port s9 s9-eth5 -- --id=@p get port s9-eth5 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s9 mirrors=@m')
	
	s10.cmd('ovs-vsctl del-port s10-eth5')
	s10.cmd('ovs-vsctl add-port s10 s10-eth5 -- --id=@p get port s10-eth5 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s10 mirrors=@m')
	
	
	s3.cmd('ovs-vsctl del-port s3-eth4')
	s3.cmd('ovs-vsctl add-port s3 s3-eth4 -- --id=@p get port s3-eth4 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s3 mirrors=@m')
	
	s4.cmd('ovs-vsctl del-port s4-eth4')
	s4.cmd('ovs-vsctl add-port s4 s4-eth4 -- --id=@p get port s4-eth4 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s4 mirrors=@m')
	
	s5.cmd('ovs-vsctl del-port s5-eth4')
	s5.cmd('ovs-vsctl add-port s5 s5-eth4 -- --id=@p get port s5-eth4 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s5 mirrors=@m')
	
	s6.cmd('ovs-vsctl del-port s6-eth4')
	s6.cmd('ovs-vsctl add-port s6 s6-eth4 -- --id=@p get port s6-eth4 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s6 mirrors=@m')
	
	
	s1.cmd('ovs-vsctl del-port s1-eth3')
	s1.cmd('ovs-vsctl add-port s1 s1-eth3 -- --id=@p get port s1-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m')
	
	
	s2.cmd('ovs-vsctl del-port s2-eth3')
	s2.cmd('ovs-vsctl add-port s2 s2-eth3 -- --id=@p get port s2-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s2 mirrors=@m')
	'''
	#________________________________________________________

	
	#packet_server(host2=h2,path="sw7.txt")
	#print('\n')
	#packet_server(host2=h3,path="sw8.txt")
	#print('\n')
	#time.sleep(3)
	
	#random.seed(12345678)
	
	counter1=random.randint(30,32)
	counter2=random.randint(30,32)
	counter3=random.randint(30,32)
	counter4=random.randint(30,32)
	counter5=random.randint(30,32)
	counter6=random.randint(30,32)
	counter7=random.randint(30,32)
	counter8=random.randint(30,32)
	'''
	counter1=random.randint(2,4)
	counter2=random.randint(2,4)
	counter3=random.randint(2,4)
	counter4=random.randint(2,4)
	counter5=random.randint(2,4)
	counter6=random.randint(2,4)
	counter7=random.randint(2,4)
	counter8=random.randint(2,4)
	'''
	#______________Find the routing________________________________________
	#client(host1=h1,host2=[h2,h3,h4,h5,h6,h7,h8],identifier=1,counter=counter1)
	#client(host1=h2,host2=[h1,h3,h4,h5,h6,h7,h8],identifier=2,counter=counter1)
	#client(host1=h3,host2=[h1,h2,h4,h5,h6,h7,h8],identifier=3,counter=counter1)
	#client(host1=h4,host2=[h1,h2,h3,h5,h6,h7,h8],identifier=4,counter=counter1)
	#client(host1=h5,host2=[h1,h2,h3,h4,h6,h7,h8],identifier=5,counter=counter1)
	#client(host1=h6,host2=[h1,h2,h3,h4,h5,h7,h8],identifier=6,counter=counter1)
	#client(host1=h7,host2=[h1,h2,h3,h4,h5,h6,h8],identifier=7,counter=counter1)
	#client(host1=h8,host2=[h1,h2,h3,h4,h5,h6,h7],identifier=8,counter=counter1)
	
	#______________Load the routes__________________________________________
	#Sending traffic from clients to servers. The same flow is sent three time
	#Each flow has a unique identifier, and the number of packets in it is based on a counter
	client(host1=h1,host2=[h5,h6,h7,h8],identifier=1,counter=counter1)
	client(host1=h2,host2=[h4,h5,h6,h7],identifier=2,counter=counter2)
	client(host1=h3,host2=[h4,h5,h7,h8],identifier=3,counter=counter3)
	client(host1=h4,host2=[h1,h2,h3,h6,h7],identifier=4,counter=counter4)
	client(host1=h8,host2=[h1,h2,h3,h4,h7],identifier=5,counter=counter5)
	client(host1=h7,host2=[h1,h3,h4,h5],identifier=6,counter=counter6)
	client(host1=h6,host2=[h2,h3,h4,h5,h7],identifier=7,counter=counter7)
	client(host1=h5,host2=[h1,h3,h4,h6],identifier=8,counter=counter8)


	
	#______________SPM_________________________________________________________
	# The port configurations are read from a file
	switch_port=read_config('./port_config.txt')
	for sw in switch_port:
		if sw=='s1':
			sw_in=s1
			spm(sniffer_interface='s1-eth3', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s2':
			sw_in=s2
			spm(sniffer_interface='s2-eth3', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s3':
			sw_in=s3
			spm(sniffer_interface='s3-eth4', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s4':
			sw_in=s4
			spm(sniffer_interface='s4-eth4', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s5':
			sw_in=s5
			spm(sniffer_interface='s5-eth4', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s6':
			sw_in=s6
			spm(sniffer_interface='s6-eth4', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s7':
			sw_in=s7
			spm(sniffer_interface='s7-eth5', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s8':
			sw_in=s8
			spm(sniffer_interface='s8-eth5', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s9':
			sw_in=s9
			spm(sniffer_interface='s9-eth5', mirroring_interface=switch_port[sw], switch=sw_in)
		elif sw=='s10':
			sw_in=s10
			spm(sniffer_interface='s10-eth5', mirroring_interface=switch_port[sw], switch=sw_in)
	
	#___________________________________________________________________________
	print('\n')
	time.sleep(3)
	client(host1=h1,host2=[h5,h6,h7,h8],identifier=1,counter=counter1)
	client(host1=h2,host2=[h4,h5,h6,h7],identifier=2,counter=counter2)
	client(host1=h3,host2=[h4,h5,h7,h8],identifier=3,counter=counter3)
	client(host1=h4,host2=[h1,h2,h3,h6,h7],identifier=4,counter=counter4)
	client(host1=h8,host2=[h1,h2,h3,h4,h7],identifier=5,counter=counter5)
	client(host1=h7,host2=[h1,h3,h4,h5],identifier=6,counter=counter6)
	client(host1=h6,host2=[h2,h3,h4,h5,h7],identifier=7,counter=counter7)
	client(host1=h5,host2=[h1,h3,h4,h6],identifier=8,counter=counter8)
	
	print('\n')
	time.sleep(3)
	
	mirroring(host2=h20,interface="h20-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h21,interface="h21-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h22,interface="h22-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h23,interface="h23-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h24,interface="h24-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h25,interface="h25-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h26,interface="h26-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h27,interface="h27-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h28,interface="h28-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])
	mirroring(host2=h29,interface="h29-eth0",dst_l=[h1,h2,h3,h4,h5,h6,h8,h7])

	print('\n')
		
	time.sleep(3)
	#if os.path.exists('./planckflow.txt'):
	#	os.remove('./planckflow.txt')
	
	client(host1=h1,host2=[h5,h6,h7,h8],identifier=1,counter=counter1)
	client(host1=h2,host2=[h4,h5,h6,h7],identifier=2,counter=counter2)
	client(host1=h3,host2=[h4,h5,h7,h8],identifier=3,counter=counter3)
	client(host1=h4,host2=[h1,h2,h3,h6,h7],identifier=4,counter=counter4)
	client(host1=h8,host2=[h1,h2,h3,h4,h7],identifier=5,counter=counter5)
	client(host1=h7,host2=[h1,h3,h4,h5],identifier=6,counter=counter6)
	client(host1=h6,host2=[h2,h3,h4,h5,h7],identifier=7,counter=counter7)
	client(host1=h5,host2=[h1,h3,h4,h6],identifier=8,counter=counter8)

	
	
	print('\n')
	time.sleep(30)#60
	
	#_________________________Sent perflow_________________________________________
	#Finding how many packtes are sent by the client
	#sent_perflow(host1=h1,host2=[h2,h3,h4,h5,h6,h7,h8],identifier=1,counter=counter1)
	
	sent_perflow(host1=h1,host2=[h5,h6,h7,h8],identifier=1,counter=counter1)
	sent_perflow(host1=h2,host2=[h4,h5,h6,h7],identifier=2,counter=counter2)
	sent_perflow(host1=h3,host2=[h4,h5,h7,h8],identifier=3,counter=counter3)
	sent_perflow(host1=h4,host2=[h1,h2,h3,h6,h7],identifier=4,counter=counter4)
	sent_perflow(host1=h8,host2=[h1,h2,h3,h4,h7],identifier=5,counter=counter5)
	sent_perflow(host1=h7,host2=[h1,h3,h4,h5],identifier=6,counter=counter6)
	sent_perflow(host1=h6,host2=[h2,h3,h4,h5,h7],identifier=7,counter=counter7)
	sent_perflow(host1=h5,host2=[h1,h3,h4,h6],identifier=8,counter=counter8)
	
	#_________________________Erite Route_________________________________
	#Routing may chnage from different runs in VM, therefore write_rout write the routes of the sent flows
	'''
	write_route(host1=h1,host2=[h5,h6,h7,h8],identifier=1,counter=counter1)
	write_route(host1=h2,host2=[h4,h5,h6,h7],identifier=2,counter=counter2)
	write_route(host1=h3,host2=[h4,h5,h7,h8],identifier=3,counter=counter3)
	write_route(host1=h4,host2=[h1,h2,h3,h6,h7],identifier=4,counter=counter4)
	write_route(host1=h8,host2=[h1,h2,h3,h4,h7],identifier=5,counter=counter5)
	write_route(host1=h7,host2=[h1,h3,h4,h5],identifier=6,counter=counter6)
	write_route(host1=h6,host2=[h2,h3,h4,h5,h7],identifier=7,counter=counter7)
	write_route(host1=h5,host2=[h1,h3,h4,h6],identifier=8,counter=counter8)
	'''
	#write_route(host1=h1,host2=[h2,h3,h4,h5,h6,h7,h8],identifier=1,counter=counter1) # case shows which routing is used
	#write_route(host1=h2,host2=[h1,h3,h4,h5,h6,h7,h8],identifier=2,counter=counter1)
	#write_route(host1=h3,host2=[h1,h2,h4,h5,h6,h7,h8],identifier=3,counter=counter1)
	#write_route(host1=h4,host2=[h1,h2,h3,h5,h6,h7,h8],identifier=4,counter=counter1)
	#write_route(host1=h5,host2=[h1,h2,h3,h4,h6,h7,h8],identifier=5,counter=counter1)
	#write_route(host1=h6,host2=[h1,h2,h3,h4,h5,h7,h8],identifier=6,counter=counter1)
	#write_route(host1=h7,host2=[h1,h2,h3,h4,h5,h6,h8],identifier=7,counter=counter1)
	#write_route(host1=h8,host2=[h1,h2,h3,h4,h5,h6,h7],identifier=8,counter=counter1)
	

	#CLI(net)
	
	
#This function writes the number of packets sent from a client to server
#Each flow has a unique identifier
def sent_perflow(host1,host2,identifier,counter):
	for host in host2:
		ip = str(host.IP())
		tmp=ip.split(".")[3]
		ident=int(tmp)*10+identifier
		file_name=str(host1)+'-'+str(host)+'.txt'
		string='sent_perflow/'+str(ident)+'.txt'
		print(str(counter), file=open(string,'a'))

#_____________________________________________________________________________________	
def packet_server(host2,path): #receiver
	print("[!] Capturing started")
	ip = str(host2.IP())
	print(ip)
	path="port_mirror/"+path
	print('sudo python3 ./server.py \"{0:s}\" \"{1:s}\"'.format(ip,path))
	host2.cmd('sudo timeout 10 python3 ./server.py \"{0:s}\" \"{1:s}\"'.format(ip,path))
	print("[+] Server cmd is done")
	

def client(host1,host2,identifier,counter):
	print("[!] Sending traffic")
	command=''
	for host in host2:
		ip = str(host.IP())
		tmp=ip.split(".")[3]
		ident=int(tmp)*10+identifier
		
		path="port_mirror/client/"+str(host1)+"-"+str(host)
		if command !='':
			command = command+ ' & ' + 'for i in {1..%d}; do sudo python3 ./client.py \"%s\" \"%s\" %d $i; done' % (counter,str(ip),path,ident)
			#command = command + '; echo "###" >> ' + path + '.txt'
			#command = command+ ' & ' + 'sudo python3 ./client.py \"%s\" \"%s\"' % (str(ip),path)
		else:
			command = 'for i in {1..%d}; do sudo python3 ./client.py \"%s\" \"%s\" %d $i;done' % (counter,str(ip),path,ident)
			#command = command + '; echo "###" >> ' + path + '.txt'
			#command = 'sudo python3 ./client.py \"%s\" \"%s\"' % (str(ip),path)
	#command = 'for i in {1..10}; do sudo python3 ./client.py \"%s\"; echo -e \'Packets sent:\t\'$i > port_mirror/stat.txt; done' % (10,str(ip),path)
		#write_flow(host1,host,ident,counter,2) # case shows which routing is used
	print(command)
	host1.cmd(command)
	
	print("[+] Client cmd is done")

#________________________________________________________________________________________
#Mirroring function is to configure sniffers to listen and capture packets from clients
def mirroring(host2,interface,dst_l):
	path="port_mirror/"+"stat_mirror_"+str(host2)+".txt"
	command=''
	for dst1 in dst_l:
		ip=dst1.IP()
		
		#print("dst: ", dst1.IP())
		if command !='':
			command = command+ ' & ' + 'python3 ./sniffer.py \"{0:s}\" \"{1:s}\" \"{2:s}\"'.format(ip,interface,path)#"10.0.0.2" "h20-eth0" "sniffer.txt"'
		else:
			command = 'python3 ./sniffer.py \"{0:s}\" \"{1:s}\" \"{2:s}\"'.format(ip,interface,path)
	command = command + '& echo "" > ' + path
	print("[!] Start Sniffing")
	host2.sendCmd(command)
	print(command)
	print("[+] Sniff ended")

#_____________________________________________________________________________________
#SPM configure a switch based on a config file	
def spm(sniffer_interface, mirroring_interface, switch):
	command= 'ovs-vsctl del-port '+sniffer_interface
	#command = 'ovs-vsctl del-port s7-eth5'
	print('mirroring command:',command)
	switch.cmd(command)
	command1= 'ovs-vsctl add-port '+str(switch)+' '+sniffer_interface
	i=1
	index_list=[]
	str_com=''
	for interface in mirroring_interface:
		 str_tmp=' -- --id=@p%d get port ' %(i)
		 #print('str tmp:',str_tmp)
		 str_com=str_tmp+interface
		 command1=command1+str_com
		 index_list.append(i)
		 i+=1
	command1=command1+' -- --id=@p get port '+sniffer_interface+' -- --id=@m create mirror name=m0 select-dst-port='
	str_com1=''

	for index in range(0,len(index_list)):
		if index+1==len(index_list):
			str_com1+='@p%d'%index_list[index]
		else:
			str_com1+='@p%d,'%index_list[index]
		
	command1=command1+ str_com1 +' output-port=@p -- set bridge '+str(switch)+' mirrors=@m'
	#command1 = 'ovs-vsctl add-port s9 s9-eth5 -- --id=@p get port s9-eth5 -- --id=@p1 get port s9-eth1 -- --id=@m create mirror name=m0 select-src-port=@p1 output-port=@p -- set bridge s7 mirrors=@m'
	print('spm command:',command1)
	switch.cmd(command1)
	

def read_config(file_name):
	switch_port=dict()
	f=open(file_name,'r')
	lines=f.readlines()
	for line in lines:
		line=line.split('\n')[0]
		key=line.split(':')[0]
		interface=key+'-'+(line.split(':')[1]).split(' ')[1]
		if key in switch_port:
			switch_port[key].append(interface)
		else:
			switch_port[key]=[interface]
	return switch_port


#__________________________________________________________________________________
#This function writes the route of a flow in planckflow.txt. I works based on find_route function from find_routing.py. It writes the path in planckflow.txt.  		
def write_route(host1,host2,identifier,counter):
	for host in host2:
		ip = str(host.IP())
		tmp=ip.split(".")[3]
		ident=int(tmp)*10+identifier
		path=find_route(str(host1),str(host),str(ident))
		counter1=counter*1250
		path[0]=path[0]-19
		path[-1]=path[-1]-19
		print(path,':',str(ident)+','+str(counter1), file=open("planckflow.txt","a"))	



if __name__=='__main__':
	FatTree()



