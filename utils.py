import math

def distance2d(p, q):
    return math.sqrt( ((p[0]-q[0])**2)+((p[1]-q[1])**2))

def distance3d(p, q):
    return math.sqrt( ((p[0]-q[0])**2)+((p[1]-q[1])**2) +((p[2]-q[2])**2))