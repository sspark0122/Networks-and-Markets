# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# given number of nodes n and probability p, output a random graph 
# as specified in homework
import random
def create_graph(n,p):
    nodes = range(n)
    graph = {node: [] for node in nodes} # key: node, value: node-edge connection
    for node in nodes:
        for neighbor in nodes[node+1:]:
            toss = random.random()
            if toss <= p:
                graph[node].append(neighbor)
                graph[neighbor].append(node)
    return graph

def create_facebook_graph(data):
    graph = {}
    for edge in data:
        a, b = edge.rstrip().split(' ')
        graph.setdefault(int(a), []).append(int(b))
        graph.setdefault(int(b), []).append(int(a))
    return graph

# given a graph G and nodes i,j, output the length of the shortest
# path between i and j in G.
def shortest_path(G,i,j):
    start, end, shortest_length = None, j, 0
    visited, queue = {i: None}, [i]
    neighbor = queue.pop(0)
    while neighbor != end:
        for i in G[neighbor]:
            queue.append(i) if i not in visited else None
            visited.setdefault(i, neighbor)
        if len(queue) == 0:
            return "infinity"
        else:
            neighbor = queue.pop(0) 

    while visited[neighbor] != None:
        shortest_length += 1
        neighbor = visited[neighbor]

    return shortest_length

# calculating the average shortest path
file = open('avg_shortest_path.txt', 'w')
count = 0
G = create_graph(1000, 0.1)
while count < 1000:
    sample = random.sample(range(1000), 2)
    length = shortest_path(G, sample[0], sample[1])
    if length != "infinity":
        count += 1
        file.write('(%s,%s,%s)\n' % (sample[0],sample[1],length))
file.close()


# varying the value of p for the random graph
file = open('varying_p.txt', 'w')
file.write('p, avg_shortest_path\n')
probs = [x*0.01 for x in range(1, 5, 1)]
for p in probs:
    count = 0
    lengths = []
    G = create_graph(1000, p)
    while count < 1000:
        sample = random.sample(range(1000), 2)
        length = shortest_path(G, sample[0], sample[1])
        if length != "infinity":
            count += 1
            lengths.append(length)
    file.write('%0.2f, %s\n' % (p, sum(lengths)/float(count)))

probs = [x*0.01 for x in range(5, 51, 5)]
for p in probs:
    count = 0
    lengths = []
    G = create_graph(1000, p)
    while count < 1000:
        sample = random.sample(range(1000), 2)
        length = shortest_path(G, sample[0], sample[1])
        if length != "infinity":
            count += 1
            lengths.append(length)
    file.write('%0.2f, %s\n' % (p, sum(lengths)/float(count)))
file.close()


# 8c) calculate the average shortest path
shortest = open('avg_shortest_path.txt').readlines()
shortest_lengths = [int(i.strip().strip('(').strip(')').split(',')[2]) for i in shortest]
print("8c) Average shortest path: ", sum(shortest_lengths)/1000.0)

# 8d) plot the average shortest paths for different probabilities
# shortest = open('varying_p.txt').readlines()[1:]
# avg_lengths = [float(i.strip().split(',')[1]) for i in shortest]
# probs = [float(i.strip().split(',')[0]) for i in shortest]

# from matplotlib import pyplot as plt
# plt.plot(probs, avg_lengths)
# plt.xlabel('Probabilities')
# plt.ylabel('Average Shortest Path')
# plt.savefig('avg_path')
# plt.show()

# facebook analysis
data = open('facebook_combined.txt', 'r').readlines()
fb_graph = create_facebook_graph(data)

file = open('fb_shortest_path.txt', 'w')
G = fb_graph
count = 0
while count < 1000:
    sample = random.sample(range(1000), 2)
    length = shortest_path(G, sample[0], sample[1])
    if length != "infinity":
        count += 1
        file.write('(%s,%s,%s)\n' % (sample[0],sample[1],length))
file.close()

# 9a) calculate average shortest path
shortest = open('fb_shortest_path.txt').readlines()
shortest_lengths = [int(i.strip().strip('(').strip(')').split(',')[2]) for i in shortest]
print('9a)Average shortest path length: ', sum(shortest_lengths)/1000.0)

# 9b) what is the probability that two random people are connected on facebook
# find the number of edges, and the number of edges with weight 1
nodes = range(len(G))
total = 0
count = 0
for node in nodes:
    for neighbor in nodes[node+1:]:
        total += 1
        if neighbor in G[node]:
            count += 1
            
print('9b)Probability: ', count/total)


# 9c) what is the average shortest path assuming the facebook graph is a random graph
count, lengths = 0, 0
G = create_graph(4038, 0.01)
while count < 1000:
    sample = random.sample(range(1000), 2)
    length = shortest_path(G, sample[0], sample[1])
    if length != "infinity":
        count += 1
        lengths += length
print('9c)Average shortest path length: ', lengths/1000.0)





