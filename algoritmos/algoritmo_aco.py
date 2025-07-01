import json
import random
import time
import os

data_dir = "dados"
with open(os.path.join(data_dir, "grafo_logistico_com_pesos.json"), "r", encoding="utf-8") as f:
    grafo = json.load(f)

with open(os.path.join(data_dir, "configuracoes_usuario.json"), "r", encoding="utf-8") as f:
    config = json.load(f)

parametros = config["aco"]
restricoes = set(config.get("restricoes", {}).get("estradas_bloqueadas", []))

arestas_lookup = {}
for a in grafo["arestas"]:
    o, d = a["origem"], a["destino"]
    arestas_lookup.setdefault(o, {})[d] = {
        "distancia_km": a["distancia_km"],
        "tempo_horas": a["tempo_horas"],
        "custo_reais": a["custo_reais"]
    }

feromonio = {}
for o in arestas_lookup:
    feromonio[o] = {d: 1.0 for d in arestas_lookup[o]}

def calcular_metricas(rota):
    dist = tempo = custo = 0
    for i in range(len(rota) - 1):
        o, d = rota[i], rota[i + 1]

        if f"{o} → {d}" in restricoes or f"{d} → {o}" in restricoes:
            return float("inf"), float("inf"), float("inf")

        aresta = arestas_lookup.get(o, {}).get(d)
        if aresta is None:
            return float("inf"), float("inf"), float("inf")

        dist += aresta["distancia_km"]
        tempo += aresta["tempo_horas"]
        custo += aresta["custo_reais"]

    return round(dist, 2), round(tempo, 2), round(custo, 2)

def calcular_probabilidades(atual, nao_visitadas):
    probabilidades = {}
    soma_total = 0.0
    for destino in nao_visitadas:
        f = feromonio.get(atual, {}).get(destino)
        aresta = arestas_lookup.get(atual, {}).get(destino)

        if f is not None and aresta is not None:
            distancia = aresta["distancia_km"]
            if distancia == 0:
                continue
            heur = 1.0 / distancia
            prob = (f ** parametros["alfa"]) * (heur ** parametros["beta"])
            probabilidades[destino] = prob
            soma_total += prob

    if soma_total == 0 and nao_visitadas:
        return {c: 1.0 / len(nao_visitadas) for c in nao_visitadas}
    return {c: p / soma_total for c, p in probabilidades.items()}

def selecionar_proxima(atual, nao_visitadas):
    probs = calcular_probabilidades(atual, nao_visitadas)
    cidades, pesos = list(probs.keys()), list(probs.values())
    return random.choices(cidades, weights=pesos, k=1)[0] if cidades else None

def atualizar_feromonio(rotas_melhores):
    for o in feromonio:
        for d in feromonio[o]:
            feromonio[o][d] *= (1 - parametros["taxa_evaporacao"])

    for rota, dist in rotas_melhores:
        if dist == float("inf"):
            continue
        deposito = parametros.get("q", 1.0) / dist
        for i in range(len(rota) - 1):
            o, d = rota[i], rota[i + 1]
            if o in feromonio and d in feromonio[o]:
                feromonio[o][d] += deposito

def aplicar_2opt(rota):
    melhor = rota[:]
    melhor_dist, _, _ = calcular_metricas(melhor)
    melhoria = True
    while melhoria:
        melhoria = False
        for i in range(1, len(melhor) - 2):
            for j in range(i + 1, len(melhor) - 1):
                nova = melhor[:i] + melhor[i:j+1][::-1] + melhor[j+1:]
                nova_dist, _, _ = calcular_metricas(nova)
                if nova_dist < melhor_dist:
                    melhor = nova
                    melhor_dist = nova_dist
                    melhoria = True
    return melhor

def executar_aco(origem="Patrocínio"):
    inicio = time.time()

    cidades = list(grafo["vertices"].keys())
    melhor_rota = None
    menor_dist = float("inf")
    top3 = []

    for iteracao in range(1, parametros["num_iteracoes"] + 1):
        rotas = []
        for _ in range(parametros["num_formigas"]):
            rota = [origem]
            nao_visitadas = set(cidades) - {origem}
            atual = origem
            while nao_visitadas:
                prox = selecionar_proxima(atual, list(nao_visitadas))
                if not prox:
                    break
                rota.append(prox)
                nao_visitadas.remove(prox)
                atual = prox
            rota.append(origem)
            dist, _, _ = calcular_metricas(rota)
            rotas.append((rota, dist))

        rotas.sort(key=lambda x: x[1])
        melhores_iteracao = rotas[:max(1, int(0.1 * parametros["num_formigas"]))]

        ajustadas = []
        for rota, dist in melhores_iteracao:
            if dist == float("inf"):
                ajustadas.append((rota, dist))
                continue
            rota_ajustada = aplicar_2opt(rota)
            dist_ajustada, _, _ = calcular_metricas(rota_ajustada)
            ajustadas.append((rota_ajustada, dist_ajustada))

        atualizar_feromonio(ajustadas)

        if ajustadas and ajustadas[0][1] < menor_dist:
            menor_dist = ajustadas[0][1]
            melhor_rota = ajustadas[0][0]

        top3.extend(ajustadas[:5])
        top3_unicas = []
        vistos = set()
        for rota, _ in sorted(top3, key=lambda x: x[1]):
            chave = tuple(rota)
            if chave not in vistos:
                vistos.add(chave)
                d, t, c = calcular_metricas(rota)
                top3_unicas.append({
                    "rota": rota,
                    "distancia_km": d,
                    "tempo_estimado_horas": t,
                    "custo_estimado_reais": c
                })
            if len(top3_unicas) == 3:
                break

        print(f"Iteração {iteracao:03d}: Melhor distância = {ajustadas[0][1]:.2f} km")

    with open(os.path.join(data_dir, "top3_aco.json"), "w", encoding="utf-8") as f:
        json.dump(top3_unicas, f, ensure_ascii=False, indent=2)

    tempo_execucao = round(time.time() - inicio, 2)
    print(f"\nACO finalizado com sucesso em {tempo_execucao:.2f} segundos.")
    print("Top 3 salvo em dados/top3_aco.json.")

    return melhor_rota, menor_dist, tempo_execucao


if __name__ == "__main__":
    executar_aco()
