import math
import numpy as np

def calc_3_circle_intersection(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    d = math.sqrt((x1-x2)**2 + (y1-y2)**2)                  # Cartesian distance
    
    if d == 0 and r1 == r2:
        raise ValueError("Error: Can't find intersection (2 circles are coincident)")
    elif d > r1 + r2:
        raise ValueError("Error: Can't find intersection (2 circles are separate)")
    elif d < abs(r1-r2):
        raise ValueError("Error: Can't find intersection (one circle contained within the other)")
    
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = math.sqrt(r1**2 - a**2)
    
    c1 = np.array([x1, y1])             # Center of circle 1 & 2
    c2 = np.array([x2, y2])             # Convert to numpy array to perform vector multiplication
    
    c3 = c1 + (a/d)*(c2-c1)             # Find c3 using c1 and c2
    c3_x = c3[0]
    c3_y = c3[1]
    
    p1_x = c3_x + (h/d)*(y2-y1)
    p1_y = c3_y - (h/d)*(x2-x1)
    
    p2_x = c3_x - (h/d)*(y2-y1)
    p2_y = c3_y + (h/d)*(x2-x1)
    
    f = lambda x, y: (x - x3)**2 + (y - y3)**2
        
    if round(f(p1_x, p1_y), 15) == round(r3**2, 15):
        intersection_point1 = p1_x
        intersection_point2 = p1_y
    elif round(f(p2_x, p2_y), 15) == round(r3**2, 15):
        intersection_point1 = p2_x
        intersection_point2 = p2_y
    else:
        raise ValueError("Error: Can't find intersection (can't find single point of intersection in all 3 circles)")
    
    return intersection_point1, intersection_point2


x, y = calc_3_circle_intersection(2, 4, 2, 5, 2, 3, 2, -3, 5)
print('p    x      y')
print(f'p1   {x:>3}   {y:>3}')