from weaver import client
c=client.Client('127.0.0.1',2002)

# for i in range(0,3):
# 	for j in range(0,3):
# 		for k in range(0,2):
# 			edges=c.get_edges(node='L2_{0}_{1}_{2}'.format(i,j,k))
# 			count=0
# 			for edge in edges:
# 				if edge.properties['edgeDirection']==['B']:
# 					count=count+1
# 			if count!=27:
# 				print i,j,k
# 				assert False
# 			else:
# 				print i,j,k,count

edges=c.get_edges(node='L2_{0}_{1}_{2}'.format(0,0,0))
count=0
for edge in edges:
	if edge.properties['edgeDirection']==['B']:
		count=count+1
if count!=27:
	print 0,0,0,count
	assert False
else:
	print 0,0,0,count



edges=c.get_edges(node='start_node'.format(0,0,0))
count=0
for edge in edges:
	if edge.properties['edgeDirection']==['F']:
		count=count+1
print count



edges=c.get_edges(node='end_node'.format(0,0,0))
count=0
for edge in edges:
	if edge.properties['edgeDirection']==['B']:
		count=count+1
print count
