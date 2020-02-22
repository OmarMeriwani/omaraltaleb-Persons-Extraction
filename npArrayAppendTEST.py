import numpy as np
import math

arr = np.array([[0.2,0.2,0.2],[3,3,3],[4,4,4]])
arr2 = [1,1,1]
print(arr)
print(arr2)
arr3 = np.zeros(shape=(arr.shape[0],arr.shape[1] + 1))
print('arr3', arr3)
for i in range(0, arr.shape[0]):
    arr3[i] = (np.append(arr[i], arr2[i]))
#arr = np.append(arr2, arr)
print(arr3)

year = 1979
radius = int(math.ceil(year / 10.0)) * 10
print(radius)

#DRAW CIRCLE
centerX = 0
Radius1 = 200
Radius2 = 400
nodes = {}
XCounter = 0
YCounter = 0
X = 0
Y = 0
degree = 20
ToggleX = False

def PointsInCircum(r,n=100):
    return [(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in range(0,n+1)]
print( [(int(n[0]), int(n[1])) for n in PointsInCircum(200, 100)])
print( [(int(n[0]), int(n[1])) for n in PointsInCircum(500, 100)])