import json,yaml
debug=True
from weaver import client
c=client.Client('127.0.0.1',2002)
def readSpec(filename):
	nn_spec=None
	with open (filename) as f:
		nn_spec=json.loads(f.read())
	nn_spec=yaml.safe_load(json.dumps(nn_spec))
	return nn_spec


def createNetwork(filename,debug=True):
	nn=readSpec(filename)
	c.begin_tx()
	c.create_node("start_node")
	c.create_node("end_node")
	if debug:
		print 'created Node:',"start_node"
		print 'created Node:',"end_node"
	# creating the nodes
	layers=nn['layers']
	for i in range(1,len(layers)+1):
		layerName='L'+str(i)
		layerElements=layers[layerName]
		for j in range(0,len(layerElements)):
			elementName=layerName+'_'+layerElements[j]
			if debug:
				print 'created Node:',elementName
			c.create_node(elementName)
			if (i==1):
				e=c.create_edge("start_node",elementName)		
				c.set_edge_properties(node="start_node", edge=e, properties={'edgeDirection':'F','weight':'1','rank':str(j)})
				e=c.create_edge(elementName,"start_node")
				c.set_edge_properties(node=elementName, edge=e, properties={'edgeDirection':'B'})
				if debug:
					print 'created edge:(e1:{0},e2:{1},weight:{2},rank:{3})'.format("start_node",elementName,'1',str(j))
			elif (i==len(layers)):
				e=c.create_edge(elementName,"end_node")
				c.set_edge_properties(node=elementName, edge=e, properties={'edgeDirection':'F','weight':'1','rank':str(j)})
				e=c.create_edge('end_node',elementName)
				c.set_edge_properties(node='end_node', edge=e, properties={'edgeDirection':'B'})
				if debug:
					print 'created edge:(e1:{0},e2:{1},weight:{2},rank:{3})'.format(elementName,"end_node",'1',str(j))

	# creating the edges
	connection=nn['connection']
	for interconnection,weights in connection.iteritems():
		layer1=interconnection.split('-')[0]
		layer2=interconnection.split('-')[1]
		for localNodes,weight in weights.iteritems():
			element1=layer1+'_'+localNodes.split('-')[0]
			element2=layer2+'_'+localNodes.split('-')[1]
			e=c.create_edge(element1,element2)
			c.set_edge_properties(node=element1, edge=e, properties={'edgeDirection':'F','weight':str(weight),'rank':'0'})
			e=c.create_edge(element2,element1)
			c.set_edge_properties(node=element2, edge=e, properties={'edgeDirection':'B'})
			if debug:
				print 'created edge:(e1:{0},e2:{1},weight:{2},rank:{3})'.format(element1,element2,str(weight),'0')
	c.end_tx()
	print 'Network Created'

def nnInference(inputVec,start_node,end_node,activationFn):
	count=0
	edges=c.get_edges(node=start_node)
	for edge in edges:
		if "edgeDirection" in edge.properties and edge.properties["edgeDirection"]==['F']:
			count=count+1
	if count!=len(inputVec):
		print "size of input incorrect"
		assert False
	return c.neuralNetInfer(input=inputVec,start_node=start_node,end_node=end_node,activationFn=activationFn)



if __name__ == '__main__':
	createNetwork("nn.json")
	print  nnInference(inputVec=[1.0,2.0,3.0],start_node="start_node",end_node="end_node",activationFn="sigmoid") 
	




