'''
Michael Tripp
CS 601/2 Capstone

NOT USED IN FINAL PROGRAM

Description: First version of my trilateration program based on
a stack exchange post. Supposedly uses linear algebra to find an
intersection by converting latitude and longitude into x y z
coordinates, although I couldn't figure out exactly how it worked
and ended up ditching this method.
'''

import math
import numpy

def trilaterate(AP_DATA):
    earthRadius = 6371 # approx authalic radius of the Earth in km
    
    # Test access point data stored in {latitude, longitude, distance(km)} tuples
    #AP_DATA = numpy.array([[37.418436, -121.963477, 0.265710701754], 
    #          [37.417243, -121.961889, 0.234592423446],
    #          [37.418692, -121.960194, 0.0548954278262]])
    AP_xyz = []
    
    # Convert geodetic Lat/Long to ECEF (cartesian coodinate system) xyz
    for i in range(len(AP_DATA)):
        
        # Convert Lat/Long to radians
        lat = math.radians(AP_DATA[i][0])
        lon = math.radians(AP_DATA[i][1])
        
        # Convert Lat/Long (in radians) to ECEF xyz
        x = earthRadius * math.cos(lat) * math.cos(lon)
        y = earthRadius * math.cos(lat) * math.sin(lon)
        z = earthRadius * math.sin(lat)
        
        xyz = [x, y, z]
        AP_xyz.append(xyz)
    
    AP_xyz = numpy.array(AP_xyz)
            
    # transform to get circle 1 at origin
    # transform to get circle 2 on x axis
    P1 = AP_xyz[0]
    P2 = AP_xyz[1]
    P3 = AP_xyz[2]
    
    DistA = AP_DATA[0][2]
    DistB = AP_DATA[1][2]
    DistC = AP_DATA[2][2]
    
    ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
    i = numpy.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
    ez = numpy.cross(ex,ey)
    d = numpy.linalg.norm(P2 - P1)
    j = numpy.dot(ey, P3 - P1)
    
    # plug and chug using above values
    x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
    y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)
    
    # only one case shown here
    z = numpy.sqrt(abs(pow(DistA,2) - pow(x,2) - pow(y,2)))
    
    triPt = P1 + x*ex + y*ey + z*ez
    
    # convert back to lat/long from ECEF, while converting radians back to degrees
    lat = math.degrees(math.asin(triPt[2] / earthRadius))
    lon = math.degrees(math.atan2(triPt[1], triPt[0]))
    
    return lat, lon

if __name__ == '__main__':
    lat, lon = trilaterate([])
    print(f"You are located at {lat} {lon}")



