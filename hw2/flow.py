# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# 8 (a)
# implement an algorithm that computes the maximum flow in a graph G
# Note: you may represent the graph, source, sink, and edge capacities
# however you want. You may also change the inputs to the function below.
# def max_flow(G, s, t, c):
#     return -1

# 8 (d)
# implement an algorithm that determines the number of edge-disjoint paths
# between two nodes in a graph G
# def edge_disjoint_paths(G, u, v):
#     return -1

import random

class Node(object):   
    def __init__(self, name, is_sink = False, cap=float('inf')):
        self.name = name
        self.is_sink = is_sink
        self.cap = cap

class Edge(object):
    def __init__(self, start, end, capacity, flow=0):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = flow
    
class Graph(object):    
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    
    def get_node(self, name):
        return self.nodes[name]
    
    def add_node(self, node):
        if node.name not in self.nodes.keys():
            self.nodes[node.name] = node
            self.edges[node.name] = []
        
    def update_edge_flow(self, start, end, capacity, flow):
        for index in range(len(self.edges[start])):
            node = self.edges[start][index]
            if node[0] == end: 
                self.edges[start][index][1] = capacity
                self.edges[start][index][2] = flow
                
    def add_edge(self, edge):
        if [edge.end, edge.capacity, edge.flow] not in self.edges[edge.start]:
            self.edges[edge.start].append([edge.end, edge.capacity, 0])
            self.add_reverse_edge(edge)
    
    def add_reverse_edge(self, edge):
        self.edges[edge.end].append([edge.start, 0, 0])
        
    def get_capacity(self, start, end):
        for node in self.edges[start]:
            if node[0] == end: return node[1], node[2]
        
    def get_edges(self, node_name):
        return [node[0] for node in self.edges[node_name] if (node[1]) > 0 ] # only get edges with capacity on them
    
    def get_filled_edges(self, node_name):
        return [node[0] for node in self.edges[node_name] if (node[2]) > 0 ] 

class DFSGraph():
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.current_path = []
        self.found = False
        self.final_path = []
        
    def set_found(self):
        self.found = False
        self.visited = set()
        self.current_path = []
        
    def get_found(self):
        return self.found

    def find_path(self, start, end):
        self.current_path.append(start)
        if start == end and self.graph.get_node(end).cap > 0:
            self.found = True
            self.graph.get_node(end).cap -= 1
            self.final_path.append(self.current_path)
            # print(self.current_path)
        for next_node in set(self.graph.get_edges(start)) - self.visited:
            if not self.found:
                self.visited.add(next_node)
                self.find_path(next_node, end)
                self.current_path = self.current_path[:-1]

    def flow(self, s, t):
        # print(s, t)
        flow_max = 0
        self.find_path(s, t) # get a path from s to t
        while self.get_found():
            path = self.final_path[-1]
            # get min capacity along this path
            cmin = min(self.graph.get_capacity(path[i], path[i+1])[0] for i in range(len(path)-1))
            flow_max += cmin
            # add the minimum capacity in the reverse direction of the residual graph
            for index in range(len(path)-1):
                cap, flow = self.graph.get_capacity(path[index], path[index+1])
                rev_cap, rev_flow = self.graph.get_capacity(path[index+1], path[index])
                self.graph.update_edge_flow(path[index+1], path[index], flow+cmin, 0) # for reverse flow
                self.graph.update_edge_flow(path[index], path[index+1], cap-(flow+cmin), flow+cmin) # forward flow
            self.set_found()
            self.find_path(s, t)
        # paths = self.actual_paths(s, t)
        return flow_max

def max_flow(G=None, s=None, t=None, E=None, cap=False):
	# E refers to all the edges, G is the graph, s is the source and t is the sink
    for edge in E:
        a, b, c = edge.rstrip().split(' ') if cap else edge.rstrip().split(' ') + ['1']
        G.add_node(Node(a))
        G.add_node(Node(b)) #G.add_node(Node(b, is_sink=True)) if b==t else 
        G.add_edge(Edge(a, b, int(c))) 
    dfs = DFSGraph(G)
    flow = dfs.flow(s, t)
    return flow

# Part 6.1
edges_1 = ['0 1 2', 's 0 1', 's 1 3', '1 t 1', '0 t 1']
# Part 6.3
edges_2 = ['s 0 1', 's 1 1', 's 2 1', 's 3 1', 's 4 1', '5 t 1', '6 t 1', '7 t 1', '8 t 1', '9 t 1', \
        '0 6 1', '2 5 1', '3 9 1', '4 7 1', '1 5 1', '1 6 1', '3 7 1', '4 8 1']
edges_3 = open('facebook_combined.txt', 'r').readlines()


def run_facebook():
    count, total_flow = 0, 0
    while count < 1000:
        G1, G2 = Graph(), Graph()
        sample = random.sample(range(4039), 2)
        if sample[0] != sample[1]:
            flow1, flow2 = max_flow(G1, str(sample[0]), str(sample[1]), edges_3), max_flow(G2, str(sample[1]), str(sample[0]), edges_3)
            count += 1
            total_flow += max(flow1, flow2)
        print('Round',count,'samples:',sample[0],sample[1], 'max flow:', max(flow1, flow2))
        # file.write('(%s,%s,%s)\n' % (sample[0],sample[1], max(flow1, flow2)))
    print('average disjoint paths:', total_flow/1000)

# assuming random nodes have to be connected
def run_facebook2():
    count, total_flow = 0, 0
    while count < 1000:
        G1, G2 = Graph(), Graph()
        sample = random.sample(range(4039), 2)
        if sample[0] != sample[1]:
            flow1, flow2 = max_flow(G1, str(sample[0]), str(sample[1]), edges_3), max_flow(G2, str(sample[1]), str(sample[0]), edges_3)
            if max(flow1, flow2) != 0:
              count += 1
              total_flow += max(flow1, flow2)
              print('Round',count,'samples:',sample[0],sample[1], 'max flow:', max(flow1, flow2))
    print('average disjoint paths:', total_flow/1000)

def run6_3():
    G = Graph()
    # items = random.sample(edges, 2)
    s1 = 's'#random.sample(items[0].split(' ')[:-1], 1)[0]
    s2 = 't'#random.sample(items[1].split(' ')[:-1], 1)[0]
    flow = max_flow(G, s1, s2, edges_2, cap=True)
    print('Part 6_3', 'samples:', s1, s2, 'MaxFlow:',flow)

def run6_1():
    G = Graph()
    # items = random.sample(edges, 2)
    s1 = 's'#random.sample(items[0].split(' ')[:-1], 1)[0]
    s2 = 't'#random.sample(items[1].split(' ')[:-1], 1)[0]
    flow = max_flow(G, s1, s2, edges_1, cap=True)
    print('Part 6_1', 'samples:', s1, s2, 'MaxFlow:',flow)

if __name__ == '__main__':
    run6_1()
    run6_3()
    # run_facebook2()
    # run_facebook()