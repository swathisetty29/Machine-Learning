import numpy as np
#Chessboard with 0 and 1

arr= np.full((10, 10), 1)
arr[1::2, ::2]=0
arr[::2, 1::2]=0
print(arr)

# 🖊️ TODO: check memory footprint of a 1000×1000 float64 array

M=np.zeros((1000,1000),dtype=np.float64)
print('shape', M.shape, 'ndim', M.ndim, 'size', M.size, 'itemsize', M.itemsize, 'total bytes', M.nbytes)

# 🖊️ TODO: use fancy indexing to swap first and last rows of `a`

a=np.arange(0,20).reshape(4,5)
print(a)
print("\n")
b=a[0,:].copy()
a[0,:]=a[3,:]
a[3,:]=b
print(a)
