import numpy as np
arr= np.full((10, 10), 1)
arr[1::2, ::2]=0
arr[::2, 1::2]=0
print(arr)
