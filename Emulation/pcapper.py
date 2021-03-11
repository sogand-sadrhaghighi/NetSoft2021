from scapy.all import RawPcapReader

def process_pcap():
    count = 0
    for (pkt_data, pkt_metadata,) in RawPcapReader("sw20"):
        count += 1
        print(pkt_data)
    print("There are that many packets: " + str(count))

if __name__=='__main__':
    process_pcap()
