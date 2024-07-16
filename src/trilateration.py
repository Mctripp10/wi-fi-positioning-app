'''
Michael Tripp
CS 601/2 Capstone

Description: program used to perform the trilateration portion
of the algorithm
'''

import math
import numpy as np
import sys
import pprint

'''
Method used to calculate the intersection of 3 circles, or output a corresponding error otherwise
    x# = center x coord of circle #
    y# = center y coord of circle #
    r# = radius of circle #
'''
def calc_3_circle_intersection(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    d = math.sqrt((x1-x2)**2 + (y1-y2)**2)                  # Cartesian distance between centers of circles 1 and 2
    
    if d == 0 and r1 == r2:
        raise ValueError("Error: Can't find intersection (2 circles are coincident)")
    elif d > r1 + r2:
        raise ValueError("Error: Can't find intersection (2 circles are separate)")
    elif d < abs(r1-r2):
        raise ValueError("Error: Can't find intersection (one circle contained within the other)")
    
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = math.sqrt(r1**2 - a**2)
    
    # Centers of circles 1 and 2, converted to numpy arrays to perform vector multiplication
    c1 = np.array([x1, y1])             
    c2 = np.array([x2, y2])             
    
     # Find center of circle 3 (c3) using c1 and c2
    c3 = c1 + (a/d)*(c2-c1)            
    c3_x = c3[0]
    c3_y = c3[1]
    
    p1_x = c3_x + (h/d)*(y2-y1)
    p1_y = c3_y - (h/d)*(x2-x1)
    
    p2_x = c3_x - (h/d)*(y2-y1)
    p2_y = c3_y + (h/d)*(x2-x1)
    
    f = lambda x, y: (x - x3)**2 + (y - y3)**2
    
    round_factor = 2
        
    if round(f(p1_x, p1_y), round_factor) == round(r3**2, round_factor):
        intersection_point1 = p1_x
        intersection_point2 = p1_y
    elif round(f(p2_x, p2_y), round_factor) == round(r3**2, round_factor):
        intersection_point1 = p2_x
        intersection_point2 = p2_y
    else:
        raise ValueError("Error: Can't find intersection (can't find single point of intersection in all 3 circles)")
    
    return intersection_point1, intersection_point2

# Method used to implement trilateration by finding the intersection of 3 circles
def trilaterate(AP_DATA):  
    c1 = [AP_DATA[0][0], AP_DATA[0][1], AP_DATA[0][2]]
    c2 = [AP_DATA[1][0], AP_DATA[1][1], AP_DATA[1][2]]
    c3 = [AP_DATA[2][0], AP_DATA[2][1], AP_DATA[2][2]]
        
    c = [c1, c2, c3]
    pprint.pprint(c)
    
    x, y = calc_3_circle_intersection(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], c3[0], c3[1], c3[2])
    return x, y

if __name__ == '__main__':
    lat, lon = trilaterate([])
    print(f"You are located at {lat} {lon}")



