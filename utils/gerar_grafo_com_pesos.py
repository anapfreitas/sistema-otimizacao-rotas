import json
import time
import itertools
import requests

API_KEY = "AIzaSyAUAUXXe_gbAEyPvT_j9RUXxcNknZVyqMg"
CONSUMO_KM_L = 10
PRECO_LITRO = 5.0

with open("dados/coordenadas_cidades.json", "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

cidades = list(coordenadas.keys())

grafo = {
    "vertices": coordenadas,
    "arestas": []
}

pares_calculados = set()

for origem, destino in itertools.combinations(cidades, 2):
    if (origem, destino) in pares_calculados or (destino, origem) in pares_calculados:
        continue

    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json?"
        f"origins={origem},MG,Brasil&destinations={destino},MG,Brasil"
        f"&language=pt-BR&units=metric&key={API_KEY}"
    )

    resposta = requests.get(url)
    dados = resposta.json()

    if dados["status"] != "OK" or dados["rows"][0]["elements"][0]["status"] != "OK":
        print(f"Erro ao buscar {origem} → {destino}")
        continue

    distancia_m = dados["rows"][0]["elements"][0]["distance"]["value"]
    tempo_s = dados["rows"][0]["elements"][0]["duration"]["value"]

    distancia_km = distancia_m / 1000
    tempo_horas = tempo_s / 3600
    custo_reais = (distancia_km / CONSUMO_KM_L) * PRECO_LITRO

    grafo["arestas"].append({
        "origem": origem,
        "destino": destino,
        "distancia_km": round(distancia_km, 2),
        "tempo_horas": round(tempo_horas, 2),
        "custo_reais": round(custo_reais, 2)
    })

    grafo["arestas"].append({
        "origem": destino,
        "destino": origem,
        "distancia_km": round(distancia_km, 2),
        "tempo_horas": round(tempo_horas, 2),
        "custo_reais": round(custo_reais, 2)
    })

    print(f"{origem} → {destino}: {round(distancia_km, 2)} km, {round(tempo_horas, 2)} h, R$ {round(custo_reais, 2)}")

    pares_calculados.add((origem, destino))
    time.sleep(2)  # Evita sobrecarga na API

with open("grafo_logistico_com_pesos.json", "w", encoding="utf-8") as f:
    json.dump(grafo, f, indent=2, ensure_ascii=False)

print("\n Arquivo grafo_logistico_com_pesos.json gerado com sucesso no novo formato!")
