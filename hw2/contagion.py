# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# Reference: 
# https://networkx.github.io/documentation/stable/reference/classes/graph.html
# https://networkx.github.io/documentation/networkx-2.1/reference/classes/generated/networkx.Graph.nodes.html
# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.Graph.neighbors.html
# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.DiGraph.number_of_nodes.html
# https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range

import networkx as nx
from helper import *
import random

# 9 (a)
# implement an algorithm that given a graph G, set of adopters S,
# and a threshold q performs BRD where the adopters S never change.
def contagion_brd(G, S, q):

	# Set X if nodes in G are initial adopters
	node_dic = {node:'Y' for node in G.nodes}
	for node in S:
		node_dic[node] = 'X'

	flag = True
	while flag:
		flag = False
		for node in G.nodes:
			if node not in S:
				num_of_X = 0
				num_of_neighbors = len(G[node])
				for neighbor in G[node]:
					if node_dic[neighbor] == 'X':
						num_of_X += 1

				if num_of_X / float(num_of_neighbors) > q and node_dic[node] != 'X':
					node_dic[node] = 'X'
					flag = True	# If any node choose X, loop one more time

	return node_dic

def is_cascade(result):
	return 'Y' not in result.values()

def get_num_infected(result):
	return sum(1 for x in result.values() if x == 'X')

def question_9a():
	# Question 9a
	print('Question 9a')
	figure_4_1a = create_figure_4_1a()
	initial_adopters = ['a']
	threshold = 0.4
	result = contagion_brd(figure_4_1a, initial_adopters, threshold)
	print('Figure 4.1a: complete cascade is {} with S = {} and threshold q = {}'.format(is_cascade(result), initial_adopters, threshold))
	print(result)

	figure_4_1a = create_figure_4_1a()
	initial_adopters = ['a']
	threshold = 0.5
	result = contagion_brd(figure_4_1a, initial_adopters, threshold)
	print('Figure 4.1a: complete cascade is {} with S = {} and threshold q = {}'.format(is_cascade(result), initial_adopters, threshold))
	print(result)

	figure_4_1b = create_figure_4_1b()
	initial_adopters = ['a', 'b', 'e']
	threshold = 0.3
	result = contagion_brd(figure_4_1b, initial_adopters, threshold)
	print('Figure 4.1b: complete cascade is {} with S = {} and threshold q = {}'.format(is_cascade(result), initial_adopters, threshold))
	print(result)

	figure_4_1b = create_figure_4_1b()
	initial_adopters = ['a', 'b', 'e']
	threshold = 0.4
	result = contagion_brd(figure_4_1b, initial_adopters, threshold)
	print('Figure 4.1b: complete cascade is {} with S = {} and threshold q = {}'.format(is_cascade(result), initial_adopters, threshold))
	print(result)

def question_9b():
	k = 10
	threshold = 0.1
	total_num_infected = 0
	fb_graph = create_fb_graph()
	for i in range(100):
		initial_adopters = random.sample(range(0, nx.number_of_nodes(fb_graph)), k)
		total_num_infected += get_num_infected(contagion_brd(fb_graph, initial_adopters, threshold))

	print('\nQuestion 9b')
	print('k:{}, q:{}, avg # of infected nodes: {}\n'.format(k, threshold, total_num_infected/float(100)))

def question_9c():
	print('Question 9c')
	thresholds = [round(x*0.05,2) for x in range(0, 11)]
	ks = [x for x in range(0, 251, 10)]
	fb_graph = create_fb_graph()
	total_num_nodes = nx.number_of_nodes(fb_graph)
	for q in thresholds:
		for k in ks:
			total_num_infected = 0
			for i in range(10):
				initial_adopters = random.sample(range(0, total_num_nodes), k)
				total_num_infected += get_num_infected(contagion_brd(fb_graph, initial_adopters, q))

			print('q:{}, k:{}, infection rate: {} (={}/{})'.format(q, k, (total_num_infected/float(10))/float(total_num_nodes), total_num_infected/float(10), total_num_nodes))

question_9a()
question_9b()
question_9c()