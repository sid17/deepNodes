from weaver import client
c=client.Client('127.0.0.1',2002)
c.begin_tx()
c.create_node("start_node")
c.create_node('1')
c.create_node('2')
c.create_node('3')
c.create_node('4')
c.create_node('5')
c.create_node('6')
c.create_node("end_node")

e=c.create_edge("start_node",'1')
c.set_edge_properties(node='start_node', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'0'})
e=c.create_edge('1',"start_node")
c.set_edge_properties(node='1', edge=e, properties={'edgeDirection':'B'})


e=c.create_edge("start_node",'2')
c.set_edge_properties(node='start_node', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'1'})
e=c.create_edge('2',"start_node")
c.set_edge_properties(node='2', edge=e, properties={'edgeDirection':'B'})


e=c.create_edge("start_node",'3')
c.set_edge_properties(node='start_node', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'2'})
e=c.create_edge('3',"start_node")
c.set_edge_properties(node='3', edge=e, properties={'edgeDirection':'B'})





e=c.create_edge("1",'4')
c.set_edge_properties(node='1', edge=e, properties={'edgeDirection':'F','weight':'2','rank':'0'})
e=c.create_edge('4',"1")
c.set_edge_properties(node='4', edge=e, properties={'edgeDirection':'B'})


e=c.create_edge("2",'5')
c.set_edge_properties(node='2', edge=e, properties={'edgeDirection':'F','weight':'3','rank':'0'})
e=c.create_edge('5',"2")
c.set_edge_properties(node='5', edge=e, properties={'edgeDirection':'B'})


e=c.create_edge("3",'6')
c.set_edge_properties(node='3', edge=e, properties={'edgeDirection':'F','weight':'4','rank':'0'})
e=c.create_edge('6',"3")
c.set_edge_properties(node='6', edge=e, properties={'edgeDirection':'B'})




e=c.create_edge("1",'5')
c.set_edge_properties(node='1', edge=e, properties={'edgeDirection':'F','weight':'2','rank':'0'})
e=c.create_edge('5',"1")
c.set_edge_properties(node='5', edge=e, properties={'edgeDirection':'B'})


e=c.create_edge("1",'6')
c.set_edge_properties(node='1', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'0'})
e=c.create_edge('6',"1")
c.set_edge_properties(node='6', edge=e, properties={'edgeDirection':'B'})












e=c.create_edge("4","end_node")
c.set_edge_properties(node='4', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'0'})
e=c.create_edge('end_node',"4")
c.set_edge_properties(node='end_node', edge=e, properties={'edgeDirection':'B'})

e=c.create_edge("5","end_node")
c.set_edge_properties(node='5', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'1'})
e=c.create_edge('end_node',"5")
c.set_edge_properties(node='end_node', edge=e, properties={'edgeDirection':'B'})



e=c.create_edge("6","end_node")
c.set_edge_properties(node='6', edge=e, properties={'edgeDirection':'F','weight':'1','rank':'2'})
e=c.create_edge('end_node',"6")
c.set_edge_properties(node='end_node', edge=e, properties={'edgeDirection':'B'})


c.end_tx()
#print c.neuralNetInfer(node='1')

