from scapy.all import *
from scapy.all import IFACES

conf.use_pcap=True

maxrssi = {}

def callBack(pkt):
    print(pkt.show())
    if pkt.haslayer(Dot11):
        print("YES")
        key = None
        if not pkt.FCfield.to_DS and pkt.FCfield.from_DS:
            if pkt.addr3 is not None:
                key = pkt.addr3
        else:
            if pkt.addr2 is not None:
                key = pkt.addr2
        if key is not None:
            if key in maxrssi.keys():
                if maxrssi[key] < pkt.dBm_AntSignal:
                    maxrssi[key] = pkt.dBm_AntSignal
                    print("NEW MAX for ", key, maxrssi[key]);
            else:
                maxrssi[key] = pkt.dBm_AntSignal
                print("NEW MAX for ", key, maxrssi[key]);

sniff(iface='Wi-Fi', prn=callBack, count=1)
for sta in maxrssi:
    print(sta, maxrssi[sta])