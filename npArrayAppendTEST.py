import numpy as np

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