import json
import random
import time


with open("dados/configuracoes_usuario.json", "r", encoding="utf-8") as f:
    config = json.load(f)["ga"]

with open("dados/grafo_logistico_com_pesos.json", "r", encoding="utf-8") as f:
    grafo = json.load(f)

cidade_origem = "Patrocínio"
cidades = list(grafo["vertices"].keys())
cidades_sem_origem = [c for c in cidades if c != cidade_origem]

populacao_tamanho = config["tamanho_populacao"]
geracoes = config["num_geracoes"]
taxa_mutacao = config["taxa_mutacao"]

grafo_arestas_dict = {}
for aresta in grafo["arestas"]:
    origem = aresta["origem"]
    destino = aresta["destino"]
    if origem not in grafo_arestas_dict:
        grafo_arestas_dict[origem] = {}
    grafo_arestas_dict[origem][destino] = aresta

_calcular_metricas_rota_cache = {}

def calcular_metricas_rota(rota):
    rota_tuple = tuple(rota)
    if rota_tuple in _calcular_metricas_rota_cache:
        return _calcular_metricas_rota_cache[rota_tuple]

    distancia = tempo = custo = 0
    for i in range(len(rota) - 1):
        o = rota[i]
        d = rota[i + 1]
        try:
            aresta = grafo_arestas_dict[o][d]
            distancia += aresta["distancia_km"]
            tempo += aresta["tempo_horas"]
            custo += aresta["custo_reais"]
        except KeyError:
            _calcular_metricas_rota_cache[rota_tuple] = (float("inf"), float("inf"), float("inf"))
            return float("inf"), float("inf"), float("inf")

    _calcular_metricas_rota_cache[rota_tuple] = (distancia, tempo, custo)
    return distancia, tempo, custo


def criar_individuo():
    meio = cidades_sem_origem[:]
    random.shuffle(meio)
    return [cidade_origem] + meio + [cidade_origem]

def selecao_torneio(populacao):
    selecionados = []
    for _ in range(len(populacao)):
        competidores = random.sample(populacao, min(3, len(populacao)))
        melhor = min(competidores, key=lambda x: calcular_metricas_rota(x)[0])
        selecionados.append(melhor)
    return selecionados

def crossover(pai1, pai2):
    meio = len(cidades_sem_origem)
    start, end = sorted(random.sample(range(1, meio + 1), 2))

    def gerar_filho(p1, p2):
        filho = [None] * (meio + 2)
        filho[0] = filho[-1] = cidade_origem
        filho[start:end+1] = p1[start:end+1]
        pos = end + 1
        for cidade in p2[1:-1]:
            if cidade not in filho:
                if pos == meio + 1:
                    pos = 1
                filho[pos] = cidade
                pos += 1
        return filho if None not in filho else p1[:]

    return gerar_filho(pai1, pai2), gerar_filho(pai2, pai1)

def mutacao(individuo):
    if random.random() < taxa_mutacao:
        i1, i2 = random.sample(range(1, len(individuo) - 1), 2)
        individuo[i1], individuo[i2] = individuo[i2], individuo[i1]
    return individuo

def aplicar_2opt(rota):
    melhor = rota[:]
    melhor_dist, _, _ = calcular_metricas_rota(melhor)
    for i in range(1, len(melhor) - 2):
        for j in range(i + 1, len(melhor) - 1):
            nova = melhor[:i] + melhor[i:j+1][::-1] + melhor[j+1:]
            nova_dist, _, _ = calcular_metricas_rota(nova)
            if nova_dist < melhor_dist:
                melhor = nova
                melhor_dist = nova_dist
    return melhor

def algoritmo_genetico():
    populacao = [criar_individuo() for _ in range(populacao_tamanho)]
    melhor_rota = None
    menor_distancia = float("inf")
    top3_raw = []

    for g in range(1, geracoes + 1):
        populacao = [ind for ind in populacao if None not in ind]
        populacao.sort(key=lambda x: calcular_metricas_rota(x)[0])
        melhor = aplicar_2opt(populacao[0])
        dist, tempo, custo = calcular_metricas_rota(melhor)

        if dist < menor_distancia:
            melhor_rota = melhor
            menor_distancia = dist

        top3_raw.append((melhor, (dist, tempo, custo)))
        top3_raw = sorted(top3_raw, key=lambda x: x[1][0])[:10]  # Mantém até 10 candidatos para garantir variedade

        pais = selecao_torneio(populacao)
        nova_geracao = []
        for i in range(0, len(pais), 2):
            p1, p2 = pais[i], pais[(i+1) % len(pais)]
            f1, f2 = crossover(p1, p2)
            nova_geracao.append(mutacao(f1))
            nova_geracao.append(mutacao(f2))
        populacao = nova_geracao[:populacao_tamanho]

        print(f"Geração {g}/{geracoes}: melhor = {dist:.2f} km")

    top3_unicas = []
    vistos = set()
    for rota, (dist, tempo, custo) in top3_raw:
        chave = tuple(rota)
        if chave not in vistos:
            vistos.add(chave)
            top3_unicas.append((rota, (dist, tempo, custo)))
        if len(top3_unicas) == 3:
            break

    return top3_unicas

if __name__ == "__main__":
    inicio = time.time()
    top3 = algoritmo_genetico()
    fim = time.time()

    resultado = []
    for rota, (dist, tempo, custo) in top3:
        resultado.append({
            "rota": rota,
            "distancia_km": round(dist, 2),
            "tempo_estimado_horas": round(tempo, 2),
            "custo_estimado_reais": round(custo, 2)
        })

    with open("dados/top3_ga.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"\nGA finalizado. Top 3 salvo em 'dados/top3_ga.json'. Tempo total: {fim - inicio:.2f}s")
