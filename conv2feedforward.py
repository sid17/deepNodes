import numpy as np
import json,yaml
from weaver import client
numNodes=0
numEdges=0
c=client.Client('127.0.0.1',2002)
def readSpec(filename):
	nn_spec=None
	with open (filename) as f:
		nn_spec=json.loads(f.read())
	nn_spec=yaml.safe_load(json.dumps(nn_spec))
	return nn_spec


def getPadding(outputDim=55,imageDim=227,filterDim=11,stride=4):
	P=((outputDim-1) * stride + filterDim - imageDim)/2
	if (P-int(P)) >0:
		assert False
	return P

def padwithzeros(vector, pad_width, iaxis, kwargs):
	vector[:pad_width[0]] = 0
	vector[-pad_width[1]:] = 0
	return vector

def getNameFromCoords(x,y,z,layer):
	return layer+'_{0}_{1}_{2}'.format(str(x),str(y),str(z))

def getFilter(filterDim,depth,numDepthFilter):
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
	if numDepthFilter==1:
		return np.asarray(l1)
	else:
		return np.asarray(l2)

def getRankFromCoords(x,y,z,imageDim,layerName):
	if layerName:
		return z*imageDim*imageDim+y*imageDim+x
	else:
		return 0


def getInterConnections(numDepthFilter,outputDim=5,imageDim=5,depth=0,filterDim=3,stride=1,inputfilter=[],layer1="",layer2=""):
	out_x=0
	out_y=0
	inputDim=imageDim
	for j in range(0,inputDim-1,stride):
		for i in range(0,inputDim-1,stride):
			for k in range(0,filterDim):
				for l in range(0,filterDim):
					for m in range(depth):
						# print '(x={0},y={1},z={2},weight={3})'.format(i+k,j+l,m,inputfilter[k][l][m]),
						createEdge(getNameFromCoords(i+k,j+l,m,layer1),getNameFromCoords(out_x,out_y,numDepthFilter,layer2),inputfilter[k][l][m],getRankFromCoords(i+k,j+l,m,imageDim,"None"))
			new_x=(out_x+1)%outputDim
			out_y=out_y+(out_x+1)/outputDim
			out_x=new_x

def createEdge(start_node,end_node,weight,rank):
	
	if start_node=="start_node":
		global numEdges
		numEdges=numEdges+1
	# print "createEdge",start_node,end_node
	c.begin_tx()
	e=c.create_edge(start_node,end_node)
	c.set_edge_properties(node=start_node, edge=e, properties={'edgeDirection':'F','weight':weight,'rank':rank})
	e=c.create_edge(end_node,start_node)
	c.set_edge_properties(node=end_node, edge=e, properties={'edgeDirection':'B'})
	c.end_tx()
def createNode(nodename):
	global numNodes
	numNodes=numNodes+1
	# print 'create node',nodename
	c.begin_tx()
	c.create_node(nodename)
	c.end_tx()

def initNetwork(filename):
	convInfo=readSpec(filename)
	layers=convInfo['layers']
	createNode("start_node")
	createNode("end_node")
	for i in range(1,len(layers)+1):
		layerName="L"+str(i)
		for x in range(0,layers[layerName]['height']):
			for y in range(0,layers[layerName]['height']):
				for z in range(0,layers[layerName]['depth']):
					nodename=getNameFromCoords(x,y,z,layerName)
					createNode(nodename)
					if (layerName=="L1"):
						createEdge("start_node",nodename,1,getRankFromCoords(x,y,z,layers[layerName]['height'],layerName))
					elif (layerName=="L"+str(len(layers))):
						createEdge(nodename,"end_node",1,getRankFromCoords(x,y,z,layers[layerName]['height'],layerName))

	if (layerName!="L1"):
		prevLayer=layers["L"+str(i-1)]
		for allFilter in range(prevLayer['numFilters']):
			inputFilter=getFilter(prevLayer['filter'],prevLayer['depth'],allFilter)
			getInterConnections(allFilter,prevLayer['outputDim'],prevLayer['height'],prevLayer['depth'],prevLayer['filter'],prevLayer['stride'],inputFilter,"L"+str(i-1),layerName)
def getInput():
	pass
	# return [,
	# ,
	# ]

def nnInference(inputVec,start_node,end_node,activationFn):
	count=0
	edges=c.get_edges(node=start_node)
	for edge in edges:
		if edge.properties["edgeDirection"]==['F']:
			count=count+1
	if count!=len(inputVec):
		print "size of input incorrect"
		assert False
	return c.neuralNetInfer(input=inputVec,start_node=start_node,end_node=end_node,activationFn=activationFn)


if __name__ == '__main__':
	# initNetwork("conv.json")
	# print numNodes
	# print numEdges
	inputVec=np.asarray(getInput())
	row0=np.asarray([[1,1,2,1,1],[0,2,1,0,2],[1,2,2,1,2],[1,1,1,1,2],[2,0,0,0,0]])
	print row0.shape
	row1=np.asarray([[0,2,0,1,1],[1,1,1,2,1],[1,1,0,2,1],[2,1,2,1,0],[2,0,1,1,1]])
	print row1.shape
	row2=np.asarray([[1,1,2,1,1],[2,2,1,0,1],[0,2,2,2,2],[2,2,1,1,1],[2,0,2,0,1]])
	print row2.shape
	processedVec=np.zeros((7,7,3))
	print np.lib.pad(row0,1,padwithzeros)
	processedVec[:,:,0]= np.lib.pad(row0,1,padwithzeros)
	processedVec[:,:,1]= np.lib.pad(row1,1,padwithzeros)
	processedVec[:,:,2]= np.lib.pad(row2,1,padwithzeros)
	inputList=processedVec[:,:,0].flatten().tolist()+processedVec[:,:,1].flatten().tolist()+processedVec[:,:,2].flatten().tolist()
	print nnInference(inputVec=inputList,start_node="start_node",end_node="end_node",activationFn="identity") 
	# print inputList
	print len(inputList)
	print processedVec[:,:,0].shape
	print processedVec
