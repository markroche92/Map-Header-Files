from graphviz import Digraph
import collections, random
from pprint import pprint

hx = {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'}

def visualise(sourceDictsList, sourceFileNames):

	graph = Digraph('G', filename='includeMap')

	with graph.subgraph(name='cluster_0') as sourceGroup:
		sourceGroup.attr('node', shape='doublecircle')
		for name in sourceFileNames: sourceGroup.node(name)

	master = dict(collections.ChainMap(*sourceDictsList))
	transUnitSets = [set(d.keys()) for d in sourceDictsList]

	# A random colour is specified for each Translation Unit
	# A final colour is specified for members of multiple Translation Units
	colourList = ["#{}{}{}{}{}{}".format(random.sample(hx, 1)[0], 
		                                 random.sample(hx, 1)[0], 
		                                 random.sample(hx, 1)[0], 
		                                 random.sample(hx, 1)[0], 
		                                 random.sample(hx, 1)[0], 
		                                 random.sample(hx, 1)[0]) for idx in range(len(sourceFileNames) + 1)]

	graph.attr('node', shape='circle')
	# Node for each file
	for k in master.keys():
		getTU = lambda x: len(sourceFileNames) if sum(x) > 1 else x.index(1)
		graph.node(k, color = colourList[getTU([1 if k in s else 0 for s in transUnitSets])])

	graph.node_attr.update(style='filled')

	for k in master.keys():
		for s in master[k]:
			graph.edge(k, s[0], label = "Line: {}".format(s[1]))

	graph.render()