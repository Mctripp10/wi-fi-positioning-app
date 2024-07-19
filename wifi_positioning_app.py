'''
Michael Tripp
CS 601/2 Capstone

Description: scans for nearby Wi-Fi access points (APs) and outputs an approximation
of user device location on a map if 3 or more scanned APs match known APs BSSIDs.
See SETUP / Configuration.
'''

import sys
import numpy as np
import collections
import itertools
import time
import matplotlib.pyplot as plt
import random
from pprint import pprint

# sys.path.append('C:/Users/Admin/Documents/College/Fall 2022/CS601/Program')
from src.windows_wlan_api import scan_APs
from src.trilateration import trilaterate


''' SETUP '''

# Configuration

map_img_path = "./resources/college_map_terrain.png"                # Enter path to map image coordinate plane and AP locations will be projected onto
top_left_corner = [99.999999, -99.999999]                           # Enter [Latitude, Longitude] coordinate of the top left corner of the map range
bottom_right_corner = [99.999999, -99.999999]                       # Enter [Latitude, Longitude] coordinate of the bottom right corner of the map range
ONLY_SHOW_MATCHES = True                                            # Set to TRUE to only show on map the known APs that match to scanned APs, otherwise show all APs
CONTINUOUS_SCAN = False                                             # Set to TRUE to continuously scan for APs and update user location in real-time, otherwise just scan once for current location

# List of all known access point MAC addresses (BSSIDs) and lat/lon locations
known_APs = [
             ["00:00:00:00:00:00", 99.99999, -99.99999],   # Test AP in the format of ["mac address", latitude, longitude]
             '''Add at least 2 more here'''
             ]

# Convert lat/lon locations of known APs to x and y and plot on coordinate plane

x_max = abs(top_left_corner[1] - bottom_right_corner[1]) * 111.320 * np.cos(41.117 * (np.pi/180)) * 1000
y_max = abs(top_left_corner[0] - bottom_right_corner[0]) * 110.574 * 1000


''' METHODS '''

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
         
# Method that converts lat/lon coordinates into x and y in meters for our predefined coordinate system. 
# See ./docs/analysis_and_discussion.pdf for more details
def convert_to_coords(lat, lon):
    x = abs(lon - top_left_corner[1]) * 111320 * np.cos(41.117 * (np.pi/180))
    y = abs(lat - bottom_right_corner[0]) * 110574
    return x, y


''' IMPLEMENTATION '''

def main(argv=None):

    # Plot all APs on map before scanning (if not only displaying matches)
    if not ONLY_SHOW_MATCHES:
        x_vals = []
        y_vals = []
        
        # Convert known AP lat/lon coords into x and y values on our map
        for AP in known_APs:
            x, y = convert_to_coords(AP[1], AP[2])
            x_vals.append(x)
            y_vals.append(y)

        img = plt.imread(map_img_path)
        fig, ax = plt.subplots()
            
        ax.imshow(img, extent=[0, x_max, 0, y_max])
        ax.plot(x_vals, y_vals, 'o', color='red', markersize = 1.5)

    while True:
        
        scanned_APs = scan_APs()        # List of all access points scanned using the windows wlan api
        sort_by_distance(scanned_APs)  
            
        AP_DATA = []
        
        # Extract data from scanned APs that match with known APs and store in AP_DATA
        for known_AP in known_APs:
            known_BSSID = known_AP[0]
            
            for scanned_AP in scanned_APs:
                scanned_BSSID = scanned_AP[0]
                
                # Match found, store in AP_DATA like as a tuple [x, y, distance] 
                if scanned_BSSID == known_BSSID:
                    distance = scanned_AP[1]
                    lat = float(known_AP[1])
                    lon = float(known_AP[2])
                    
                    x, y = convert_to_coords(lat, lon)
                    
                    data = [x, y, distance]
                    AP_DATA.append(data)
                    break
        
        # Plot matched APs on map (if only displaying matches)
        if ONLY_SHOW_MATCHES:
            x_vals = []
            y_vals = []
        
            for AP in AP_DATA:
                x_vals.append(AP[0])
                y_vals.append(AP[1])
                
            img = plt.imread(map_img_path)
            fig, ax = plt.subplots()
            ax.imshow(img, extent=[0, x_max, 0, y_max])
            ax.plot(x_vals, y_vals, 'o', color='red', markersize = 1.5)
        
        # Stop if < 3 matches found
        if len(AP_DATA) < 3:
            print(f"AP Count {len(AP_DATA)}: Not enough access points detected to determine location")
        # Otherwise, trilaterate user position by finding a weighted average of all 3-group AP combination coordinate estimates
        else:            
            combinations = list([list(comb) for comb in itertools.combinations(AP_DATA, 3)])        # Store all combinations of APs in AP_DATA of size 3
            coordinates = []
            
            # Determine user device coordinate estimate for each 3-group AP combination
            for comb in combinations:
                user_x, user_y = trilaterate(comb)
                coordinates.append([user_x, user_y])
                
            total_x = 0
            total_y = 0
            total_weight = 0
            n = len(coordinates)

            # Determine weighted average of all coordinates
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
            
            # Plot result and print coordinates to console

            plt.scatter(x_vals, y_vals)
            plt.show()
            
            print("You are located at {}, {}!".format(weighted_avg_x, weighted_avg_y))
            ax.plot(weighted_avg_x, weighted_avg_y, 'o', color='blue', markersize = 0.5)
        if not CONTINUOUS_SCAN:
            break
        time.sleep(0.2)

if __name__ == "__main__":
     sys.exit(main(sys.argv))

        
        
        


