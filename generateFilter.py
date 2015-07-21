import numpy as np
# identity=np.mat(np.eye(filterDim))
# Imfilter=np.zeros((filterDim,filterDim,depth))
# for i in range(depth):
# 	Imfilter[:,:,i]=identity
# return Imfilter
l1=[
[[1,1,0],[1,0,1],[-1,1,1]],
[[-1,0,1],[-1,0,0],[-1,0,1]],
[[0,-1,-1],[-1,1,0],[0,0,0]]
]


l2=[
[[-1,0,1],[-1,0,1],[0,0,-1]],
[[0,1,0],[-1,1,0],[-1,0,1]],
[[0,-1,-1],[-1,1,0],[-1,-1,0]]
]

print np.asarray(l1)
print np.asarray(l2)