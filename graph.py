import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt
import random
import time
import math
src=1#Enter the source
des=225#Enter the destination
rang=226#Enter the number of nodes+1
root=int(math.sqrt(rang-1))
t_max=20
randoms=0#1 for a square grid, 0 for a random grid


g=nx.Graph()

node=range(1,rang)
g.add_nodes_from(node)

def goto(linenum):
    global line
    line = linenum

# g.add_node(1)
# g.add_node(2)
# g.add_node(3)
# g.add_node(4)
# g.add_node(5)
# g.add_nodes_from([1,5])
# g.add_edge(1,2,color='g',weight=40,length=40)
# g.add_edge(1,3,color='g',weight=50,length=50)
# g.add_edge(3,4,color='r',weight=60,length=60)
# g.add_edge(2,5,color='r',weight=70,length=70)
# g.add_edge(5,3,color='g',weight=80,length=80)
# edges=g.edges()
#colors = [g[u][v]['color'] for u,v in edges]
#weights = [g[u][v]['weight'] for u,v in edges]
if randoms:
	pos=nx.random_layout(g)
	rang=rang-1
	root=int(math.sqrt(rang))
else:
	rang=rang-1
	root=int(math.sqrt(rang))
	fixed_pos={}
	for i in range(root):
	    for j in range(root):
        	fixed_pos[i*root+j+1]=(2*j,2*i)#Defining fixed position of the nodes

	fixed_nodes =fixed_pos.keys()#dont change
	pos=nx.spring_layout(g,pos=fixed_pos,fixed=fixed_nodes)#fixing the layour

d=[src,des]										#initialization of visited matrix
rndms=[src,src+1,src-root,src+root]				#inititalization of the domain of values from which a random number can be picked, works near source, contatins all the values of node to be visited
rndmd=[des,des+1,des-root,des+root]				#inititalization of the domain of values from which a random number can be picked, works near destination
used=1											#Used to alternate between source and desitination files
strt1=time.time()
inde=1
trigger=0
while(1):
	strt=time.time()
	xclude=range(121+inde%7,130+inde%7)			#Range of values for which there is an obstacle
	inde=inde+1									#to include randomness in xclude matrix
	r=[]
	for i in xclude:
		r=r+range(i,i+5*root,root)
	xclude=r+xclude
	#print ("rndms:",rndms)
	#print ("rndmd:",rndmd)
	if len(rndms)==0 and len(rndmd)==0:			#Stopping condition
		trigger=1
		print ("###################################")
		if nx.has_path(y,src,des):
			print ("Solution is :", path, " in ",stop-strt1, " seconds")
		else:
			print("No path")

	if trigger==0:	
		if len(rndms)==0 and used==1:
			used=0
			continue
		if len(rndmd)==0 and used==0:
			used=1
			continue
		if used==1:
			k=random.choice(rndms)					#Random value generator from the near source visited matrix
			if k<=0 or k>rang:						#Check condtion that whether the number lies is range
				rndms.remove(k)						#Delete if not in range
				continue
			rndms.remove(k)							#As the node is visited it is remobed
			if k in rndmd:
				rndmd.remove(k)
		if used==0:
			k=random.choice(rndmd)					#same as above
			if k<=0 or k>rang:
				rndmd.remove(k)
				continue
			rndmd.remove(k)
			if k in rndms:
				rndms.remove(k)
		flag=0											#Default value of flag, value will be added only if flag is one
		for i in range(len(d)):
			if(k==d[i]+root or k==d[i]-root or k==d[i]+1 or k==d[i]-1):#Check condition whether an edge is valid
				if((k==d[i]+1 and d[i]%root==0) or (k==d[i]-1 and d[i]%root==1)):#invalid condtition
					flag=0
				else:
					g.add_edge(k,d[i],color='g',weight=40,length=40)			#for valid conditions add edge
					flag=1
					#print (k,d[i]+root,d[i]-root,d[i]+1,d[i]-1)
			if(k==d[i]):
				flag=0
		if flag==1:
			if k not in d:								#if k is not in visited matrix
				d.append(k)
			addi=[k+1,k+root,k-root,k-1]				#Add values near to it to be visited
			if used==1:
				if k+1 in rndms or k+1 in d or k+1 in xclude:	#Remove condition, already in rndms, or already visited, or is in xclude matrix
					addi.remove(k+1)
				if k-1 in rndms or k-1 in d or k-1 in xclude:	#Conditions in wich it has to be removed, 
					addi.remove(k-1)
				if k+root in rndms or k+root in d or k+root in xclude:
					addi.remove(k+root)
				if k-root in rndms or k-root in d or k-root in xclude:
					addi.remove(k-root)		
				rndms.extend(addi)
				used=0
			else:
				if k+1 in rndmd or k+1 in d or k+1 in xclude:
					addi.remove(k+1)
				if k-1 in rndmd or k-1 in d or k-1 in xclude:
					addi.remove(k-1)
				if k+root in rndmd or k+root in d or k+root in xclude:
					addi.remove(k+root)
				if k-root in rndmd or k-root in d or k-root in xclude:
					addi.remove(k-root)	
				rndmd.extend(addi)
				used=1

				#print (d,k)
				
			# plt.ion()
			# plt.show()
			# plt.pause(5)
			# plt.clf()
		
	edges=g.edges()
	colors = [g[u][v]['color'] for u,v in edges]
	weights = [g[u][v]['weight'] for u,v in edges]
	nx.draw(g, pos, edges=edges, edge_color=colors, width=1, with_labels=False,node_size=20)
	nx.draw_networkx_nodes(g,pos, nodelist=xclude,node_color='yellow',node_size=30,alpha=0.8)
	y=g.copy()												#Graph copy
	y.remove_nodes_from(xclude)								#Nodes that cant be visited
	if nx.has_path(y,src,des):
		stop=time.time()
		print (nx.shortest_path(y,source=src,target=des,weight="weight"))
		path = nx.shortest_path(y,source=src,target=des,weight="weight") #Shortest parth printing from y
		path_edges = list(zip(path,path[1:]))
		nx.draw_networkx_nodes(g,pos,nodelist=path)
		nx.draw_networkx_edges(g,pos,edgelist=path_edges,edge_color='black',width=5,arrows=True,style='dashdot')#display from x
	#print "###############################"
	plt.ion()
	plt.savefig("Graph2.png", dpi=None, bbox_inches='tight') #Graph into picture
	plt.show()
	plt.pause(0.001)
	plt.clf()
	#print time.time()-strt									#computational time

