import json
import matplotlib.pyplot as plt
import os

caminho_aco = os.path.join("dados", "top3_aco.json")
caminho_ga = os.path.join("dados", "top3_ga.json")

with open(caminho_aco, "r", encoding="utf-8") as f:
    dados_aco = json.load(f)
with open(caminho_ga, "r", encoding="utf-8") as f:
    dados_ga = json.load(f)

rotulos = [f"Rota {i+1}" for i in range(3)]
x = range(len(rotulos))
largura = 0.35

dist_aco = [r["distancia_km"] for r in dados_aco]
dist_ga = [r["distancia_km"] for r in dados_ga]

tempo_aco = [r["tempo_estimado_horas"] for r in dados_aco]
tempo_ga = [r["tempo_estimado_horas"] for r in dados_ga]

custo_aco = [r["custo_estimado_reais"] for r in dados_aco]
custo_ga = [r["custo_estimado_reais"] for r in dados_ga]

def desenhar_grafico(titulo, valores_aco, valores_ga, ylabel):
    fig, ax = plt.subplots()
    cores_aco = "#E75480"  
    cores_ga = "#FFB6C1"  

    barras_aco = ax.bar([i - largura/2 for i in x], valores_aco, width=largura, label="ACO", color=cores_aco)
    barras_ga = ax.bar([i + largura/2 for i in x], valores_ga, width=largura, label="GA", color=cores_ga)

    for barra in barras_aco + barras_ga:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, altura + 0.2, f'{altura:.2f}', ha='center', va='bottom', fontsize=8)

    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos)
    ax.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

desenhar_grafico("Comparação de Distâncias (km)", dist_aco, dist_ga, "Distância (km)")
desenhar_grafico("Comparação de Tempo Estimado (h)", tempo_aco, tempo_ga, "Tempo (h)")
desenhar_grafico("Comparação de Custo Estimado (R$)", custo_aco, custo_ga, "Custo (R$)")
