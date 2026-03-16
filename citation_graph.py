import networkx as nx
import plotly.graph_objects as go
import re


def extract_citations(text):

    citations = re.findall(r'\[(\d+)\]', text)

    return list(set(citations))


def build_graph(citations):

    G = nx.Graph()

    main_paper = "Uploaded Paper"

    for c in citations:
        G.add_edge(main_paper, f"Paper {c}")

    return G


def plot_graph(G):

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)

        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines'
    ))

    return fig