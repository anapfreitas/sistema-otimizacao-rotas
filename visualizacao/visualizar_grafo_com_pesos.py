import json
import networkx as nx
import matplotlib.pyplot as plt


with open("dados/grafo_logistico_com_pesos.json", "r", encoding="utf-8") as f:
    grafo = json.load(f)

vertices = grafo["vertices"]
arestas = grafo["arestas"]
cidade_origem = "Patrocínio"


def plotar_grafo_por_metrica(metrica, titulo, label_fmt):
    G = nx.DiGraph()

    
    for cidade, coord in vertices.items():
        G.add_node(cidade, pos=(coord["lng"], -coord["lat"]))

    
    pesos = []
    for aresta in arestas:
        if aresta["origem"] == cidade_origem:
            destino = aresta["destino"]
            valor = aresta[metrica]
            pesos.append(valor)
            rotulo = label_fmt.format(valor)
            G.add_edge(cidade_origem, destino, weight=valor, label=rotulo)

    
    pos = nx.spring_layout(G, seed=42, k=2.5)

    plt.figure(figsize=(6, 4))
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color="#d0e1ff")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    larguras = [w / max(pesos) * 4 for w in pesos]
    nx.draw_networkx_edges(G, pos, width=larguras, edge_color="black", arrowstyle="-|>", arrowsize=15)

    labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=9)

    plt.title(titulo, fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


plotar_grafo_por_metrica("distancia_km", "Conexões de Patrocínio - Distâncias (km)", "{:.1f} km")
plotar_grafo_por_metrica("tempo_horas", "Conexões de Patrocínio - Tempos Estimados (h)", "{:.1f} h")
plotar_grafo_por_metrica("custo_reais", "Conexões de Patrocínio - Custos Estimados (R$)", "R${:.2f}")
