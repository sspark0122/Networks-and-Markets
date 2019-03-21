import networkx as nx

# Create a graph in Figure 4.1.a
# Reference: https://networkx.github.io/documentation/stable/reference/classes/graph.html
def create_figure_4_1a():
	G = nx.Graph()
	G.add_edge('a', 'b')
	G.add_edge('b', 'c')
	G.add_edge('c', 'd')
	
	return G

# Create a graph in Figure 4.1.b
def create_figure_4_1b():
	G = nx.Graph()
	G.add_edge('a', 'b')
	G.add_edge('b', 'e')
	G.add_edge('b', 'c')
	G.add_edge('c', 'f')
	G.add_edge('c', 'd')
	G.add_edge('d', 'g')

	return G

# Create a graph from facebook_combined.txt
def create_fb_graph():
	node_pairs = []
	file = open('facebook_combined.txt', 'r')
	for line in file:
		temp = line.split()
		temp[0] = int(temp[0])
		temp[1] = int(temp[1])
		node_pairs.append(temp)

	fb_graph = nx.Graph()
	for pair in node_pairs:
		fb_graph.add_edge(pair[0], pair[1])

	return fb_graph