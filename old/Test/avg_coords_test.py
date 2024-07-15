from itertools import combinations
import numpy as np

for known_AP in known_APs:
    known_BSSID = known_AP[0]
    
    for scanned_AP in scanned_APs:
        scanned_BSSID = scanned_AP[0]
        
        if scanned_BSSID == known_BSSID:
            distance = scanned_AP[1]
            lat = float(known_AP[1])
            lon = float(known_AP[2])
            
            data = [lat, lon, distance]
            AP_DATA.append(data)
            break
        
if len(AP_DATA) < 3:
    print(f"AP Count {len(AP_DATA)}: Not enough access points detected to determine location")
else:
    combinations = [",".join(map(str, comb)) for comb in combinations(AP_DATA, 3)]
    coordinates = []
    
    for comb in combinations:
        comb = np.array(comb)
        user_lat, user_lon = trilaterate(comb)
        coordinates.append([user_lat, user_lon])
        
    total_lat = total_lon = 0
    for latlon in coordinates:
        lat = latlon[0]
        lon = latlon[1]
        
        total_lat += lat
        total_lon += lon
    
    n = len(coordinates)
    average_lat = total_lat/n
    average_lon = total_lon/n
    
    print("You are located at {}, {}!".format(average_lat, average_lon))
    
    
    
    
    
    
    
    
    
    
    
    
count = 0

for known_AP in known_APs:
    known_BSSID = known_AP[0]
    lat = float(known_AP[1])
    lon = float(known_AP[2])
    
    # Collect the 3 APs with the greatest signal strength
    i = 0
    while i < len(scanned_APs):    
        scanned_AP = scanned_APs[i]
        scanned_BSSID = scanned_AP[0]
        
        if scanned_BSSID == known_BSSID:
            distance = scanned_AP[1]
            data = [lat, lon, distance]
            AP_DATA.append(data)
            count += 1
            break
        i += 1
    if count >= 3:
        break
if count < 3:
    print(f"AP Count {count}: Not enough access points detected to determine location")
else:
    AP_DATA = np.array(AP_DATA)
    
    user_lat, user_lon = trilaterate(AP_DATA)
    print("You are located at {}, {}!".format(user_lat, user_lon))
        
        
        
    