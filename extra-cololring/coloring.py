import matplotlib.pyplot as plt
import networkx as nx

def simplify(graph, colors): #FUNKAR
    graph_copy = graph.copy()
    stack = []
    while True:
        removed_node = None
        for node in graph_copy.nodes():
            if len(graph_copy[node]) < len(colors):
                graph_copy.remove_node(node)
                stack.append(node)
                removed_node = node
                break
        if not removed_node:
            break
    return stack

def rebuild(graph, stack, colors):
    color_map = {}
    for node in reversed(stack):
        used_colors = [color_map[neighbor] for neighbor in graph[node] if neighbor in color_map]
        available_colors = [color for color in colors if color not in used_colors]
        color_map[node] = available_colors[0]
    return color_map

def viz_color_graph(graph, colors):
    stack = simplify(graph, colors)
    color_map = rebuild(graph, stack, colors)

    node_colors = [color_map[node] for node in graph.nodes()]
    nx.draw(graph, node_color=node_colors)
    plt.show()

def demo():
    G = nx.Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    viz_color_graph(G, ['red', 'green', 'blue'])

if __name__ == '__main__':
    demo()
