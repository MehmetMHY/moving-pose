import matplotlib.pyplot as plt # using matplotlib for displaying graph
import networkx as nx # using NetworkX to create, manage, and search though graph

G = nx.Graph() # set NetworkX graph object
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(3, 5)
G.add_edge(3, 9)
G.add_edge(5, 6)
G.add_edge(6, 7)
G.add_edge(7, 8)
G.add_edge(9, 10)
G.add_edge(10, 11)
G.add_edge(11, 12)
G.add_edge(1, 17)
G.add_edge(17, 18)
G.add_edge(18, 19)
G.add_edge(19, 20)
G.add_edge(1, 13)
G.add_edge(13, 14)
G.add_edge(14, 15)
G.add_edge(15, 16)

n = list(nx.bfs_edges(G, source=1))
print(n)

nx.draw(G, with_labels=True, pos=nx.random_layout(G)) # draws graph
plt.show()



