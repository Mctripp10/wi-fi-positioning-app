from scapy.all import *

# sniff a packet from the interface
pkt = sniff(iface='wlan0', count=1)
pkt.show()
pkt = pkt[0]

#radiotap = pkt.getlayer(RadioTap)
#rssi = radiotap.dBm_AntSignal
#pkt = pkt[0]







# getting the RSSI
print(pkt.haslayer(RadioTap))
radiotap = pkt.getlayer(RadioTap)
rssi = radiotap.dBm_AntSignal
print("RSSI={}".format(rssi)) # RSSI=-84