import operator

import networkx as nx
import matplotlib.pyplot as plt


def powerlaw_network_graph(nodes, gamma):
    # create a graph with degrees following a power law distribution
    s = nx.utils.powerlaw_sequence(nodes, gamma)
    G = nx.expected_degree_graph(s, selfloops=False)

    return G


def degree_attack(G):
    G = G.copy()
    comp_size = [(0, [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)][0])]
    for i in range(1, len(G.nodes())):
        big_node = max(G.degree(), key=lambda x: x[1])
        G.remove_node(big_node[0])
        comp_size.append((i, [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)][0]))

    return comp_size


def clustering_attack(G):
    G = G.copy()
    comp_size = [(0, [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)][0])]
    for i in range(1, len(G.nodes())):
        big_node = max(nx.clustering(G).items(), key=operator.itemgetter(1))
        G.remove_node(big_node[0])
        comp_size.append((i, [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)][0]))

    return comp_size


def hierarchical_network_graph(base_size, level):
    """Generate the hierarchical network structure needed for Problem 1.

    Parameters
    ----------

    base_size (int)
        The number of the nodes in the clique that is used as the
        base of the model.

    level (int)
        The number of replications to create. For example, if base_size=5,
        level=2 creates a network with 25 nodes.

    Returns
    -------

    G (nx.Graph)
        A graph generated via the hierachical model.
    """
    G = nx.complete_graph(base_size)
    for n in G.nodes():
        if n > 0:
            G.nodes[n]['peripheral'] = True
        else:
            G.nodes[n]['peripheral'] = False

    for i in range(level - 1):
        gs = [G.copy() for _ in range(base_size - 1)]
        for n in G.nodes():
            G.nodes[n]['peripheral'] = False
        for g in gs:
            G = nx.disjoint_union(G, g)
        for n in G.nodes():
            if G.nodes[n]['peripheral'] == True:
                G.add_edge(n, 0)
    return G


def main():
    pl_graph = powerlaw_network_graph(3125, 2.5)
    pl_degree = degree_attack(pl_graph)
    pl_clustering = clustering_attack(pl_graph)
    print(pl_degree)
    print(pl_clustering)

    hier_graph = hierarchical_network_graph(5, 5)
    hier_degree = degree_attack(hier_graph)
    hier_clustering = clustering_attack(hier_graph)
    print(hier_degree)
    print(hier_clustering)

    # Degree Based Attack
    plt.plot([pl[0]/len(pl_graph.nodes()) for pl in pl_degree], [pl[1] for pl in pl_degree], label="Powerlaw Graph")
    plt.plot([hier[0]/len(hier_graph.nodes()) for hier in hier_degree], [hier[1] for hier in hier_degree], label="Hierarchical Graph")
    plt.title('Degree Based Attack')
    plt.xlabel('Percent of Nodes Removed')
    plt.ylabel('Largest Component Size')
    plt.legend()
    plt.savefig('pics/degree.png')
    plt.close()

    # Clustering Based Attack
    plt.plot([pl[0]/len(pl_graph.nodes()) for pl in pl_clustering], [pl[1] for pl in pl_clustering], label="Powerlaw Graph")
    plt.plot([hier[0]/len(hier_graph.nodes()) for hier in hier_clustering], [hier[1] for hier in hier_clustering], label="Hierarchical Graph")
    plt.title('Clustering Based Attack')
    plt.xlabel('Percent of Nodes Removed')
    plt.ylabel('Largest Component Size')
    plt.legend()
    plt.savefig('pics/clustering.png')
    plt.close()

    # Powerlaw Attacks
    plt.plot([pl[0]/len(pl_graph.nodes()) for pl in pl_degree], [pl[1] for pl in pl_degree], label="Degree Attack")
    plt.plot([pl[0]/len(pl_graph.nodes()) for pl in pl_clustering], [pl[1] for pl in pl_clustering], label="Clustering Attack")
    plt.title('Powerlaw Attacks')
    plt.xlabel('Percent of Nodes Removed')
    plt.ylabel('Largest Component Size')
    plt.legend()
    plt.savefig('pics/powerlaw.png')
    plt.close()

    # Hierarchical Attacks
    plt.plot([hier[0]/len(hier_graph.nodes()) for hier in hier_degree], [hier[1] for hier in hier_degree], label="Degree Attack")
    plt.plot([hier[0]/len(hier_graph.nodes()) for hier in hier_clustering], [hier[1] for hier in hier_clustering], label="Clustering Attack")
    plt.title('Hierarchical Attacks')
    plt.xlabel('Percent of Nodes Removed')
    plt.ylabel('Largest Component Size')
    plt.legend()
    plt.savefig('pics/hierarchical.png')
    plt.close()


if __name__ == '__main__':
    main()
