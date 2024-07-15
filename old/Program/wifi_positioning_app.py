'''
Michael Tripp
CS 601/2 Capstone

Description: program containing all main code for implementing
the Wi-Fi trilateration algorithm and used to store access point
data.
'''

import sys
import numpy as np
import collections
import itertools
import time
import matplotlib.pyplot as plt
import random
from pprint import pprint

sys.path.append('C:/Users/Admin/Documents/College/Fall 2022/CS601/Program')
from windows_wlan_api import scan_APs
from trilateration2 import trilaterate


''' Methods '''


# Insertion sort algorithm to sort AP data by distance
def sort_by_distance(a):
    if (n := len(a)) <= 1:
        return
    for i in range(1, n):        
        key = a[i]
        
        j = i-1
        while j >= 0 and key[1] < a[j][1]:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
        
# Method that converts lat/lon coordinates into x and y for our predefined coordinate system in meters
def convert_to_coords(lat, lon):
    x = abs(lon - top_left_corner[1]) * 111320 * np.cos(41.117 * (np.pi/180))
    y = abs(lat - bottom_right_corner[0]) * 110574
    return x, y


''' Setup '''


# List of all known access point MAC addresses and lat/lon locations

known_APs = [
             ["E8:26:89:1E:06:40", 41.11900, -80.33260],   # MG.b.G03.i
             ["E8:26:89:1E:06:50", 41.11906, -80.33262],   # MG.AP72
             ["E8:26:89:1F:1C:10", 41.11893, -80.33279],   # MG.1.101.i 
             ["E8:26:89:1F:1C:01", 41.11900, -80.33260],   # MG.b.G03.i
             ["E8:26:89:1D:08:41", 41.11906, -80.33262],   # MG.AP72
             ["E8:26:89:1D:5F:00", 41.11893, -80.33279],   # MG.1.101.i 
             
             ["D0:D3:E0:5B:6F:50", 41.119163, -80.328689],   # H.2.257.i        
             ["D0:D3:E0:5B:DD:A0", 41.119223, -80.328696],   # h.2.258.i
             ["D0:D3:E0:5C:EF:30", 41.11960, -80.32853],   # Hoyt.1.130.o
             ["E8:26:89:1E:35:50", 41.11948, -80.32856],   # H.1.138.i
             ["D0:D3:E0:5B:56:10", 41.11903, -80.32839],   # H.Chem.1.180.o    
             ["D0:D3:E0:5B:E7:90", 41.11968, -80.32885],   # H.1.119.i
             ["D0:D3:E0:5C:AF:70", 41.119170, -80.328735],  # H.2.257.o        
             ["D0:D3:E0:5C:E6:90", 41.119078, -80.328905],  # H.2.nur.o        
             ["D0:D3:E0:5B:9D:B0", 41.11921, -80.32865],   # H.1.162.i
             ["D0:D3:E0:5B:B5:90", 41.11921, -80.32899]    # H.1.ele.o        
             ]

# Convert lat/lon locations of known APs to x and y and plot on coordinate plane

top_left_corner = [41.120140, -80.332992]
bottom_right_corner = [41.117155, -80.327708]
x_max = abs(top_left_corner[1] - bottom_right_corner[1]) * 111.320 * np.cos(41.117 * (np.pi/180)) * 1000
y_max = abs(top_left_corner[0] - bottom_right_corner[0]) * 110.574 * 1000

ONLY_SHOW_MATCHES = True

if not ONLY_SHOW_MATCHES:
    x_vals = []
    y_vals = []
    
    for AP in known_APs:
        x, y = convert_to_coords(AP[1], AP[2])
        x_vals.append(x)
        y_vals.append(y)

    img = plt.imread("C:/Users/Admin/Documents/College/Fall 2022/CS601/Documentation/College_Map_Terrain.png")
    fig, ax = plt.subplots()
        
    ax.imshow(img, extent=[0, x_max, 0, y_max])
    ax.plot(x_vals, y_vals, 'o', color='red', markersize = 1.5)

''' Implementation '''


TOP_THREE = 0
WEIGHTED_AVG = 1
LEAST_SQUARES = 2

METHOD = WEIGHTED_AVG

loop_once = True

while True:
    
    scanned_APs = scan_APs()        # List of all access points scanned using the windows wlan api
    sort_by_distance(scanned_APs)   # Sort by distance
        
    
    AP_DATA = []
    
    for known_AP in known_APs:
        known_BSSID = known_AP[0]
        
        for scanned_AP in scanned_APs:
            scanned_BSSID = scanned_AP[0]
            
            if scanned_BSSID == known_BSSID:
                distance = scanned_AP[1]
                lat = float(known_AP[1])
                lon = float(known_AP[2])
                
                x, y = convert_to_coords(lat, lon)
                
                data = [x, y, distance]
                AP_DATA.append(data)
                break
    
    if ONLY_SHOW_MATCHES:
        x_vals = []
        y_vals = []
    
        for AP in AP_DATA:
            x_vals.append(AP[0])
            y_vals.append(AP[1])
            
        img = plt.imread("C:/Users/Admin/Documents/College/Fall 2022/CS601/Documentation/College_Map_Terrain.png")
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[0, x_max, 0, y_max])
        ax.plot(x_vals, y_vals, 'o', color='red', markersize = 1.5)
            
    if len(AP_DATA) < 3:
        print(f"AP Count {len(AP_DATA)}: Not enough access points detected to determine location")
    else:
        if METHOD == WEIGHTED_AVG:
            combinations = list([list(comb) for comb in itertools.combinations(AP_DATA, 3)])
            coordinates = []
            
            for comb in combinations:
                user_x, user_y = trilaterate(comb)
                coordinates.append([user_x, user_y])
                
            total_x = 0
            total_y = 0
            total_weight = 0
            n = len(coordinates)

            for i in range(n):
                x = coordinates[i][0]
                y = coordinates[i][1]
                
                total_x += (n-i) * x
                total_y += (n-i) * y
                total_weight += n-i
            
            weighted_avg_x = total_x/total_weight
            weighted_avg_y = total_y/total_weight
            x_vals.append(weighted_avg_x)
            y_vals.append(weighted_avg_y)
            
            plt.scatter(x_vals, y_vals)
            plt.show()
            
            print("You are located at {}, {}!".format(weighted_avg_x, weighted_avg_y))
            ax.plot(weighted_avg_x, weighted_avg_y, 'o', color='blue', markersize = 0.5)

        elif METHOD == LEAST_SQUARES:
            n = len(AP_DATA)
            sum_x = 0       
            sum_y = 0
            sum_xy = 0
            sum_x2 = 0
            
            for AP in AP_DATA:
                x = AP[0]
                y = AP[1]
                
                sum_x += x       
                sum_y += y
                sum_xy += x * y
                sum_x2 += x * x
                
            m = (n * sum_xy - sum_x * sum_y)/(n * sum_x2 - sum_x**2)
            b = (sum_y - m * sum_x)/n
            
    if loop_once:
        break
    time.sleep(0.2)


        
        
        


