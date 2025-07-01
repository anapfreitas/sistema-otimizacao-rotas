# 📍 Sistema de Otimização de Rotas Logísticas

Este projeto implementa um sistema inteligente para **otimização de rotas logísticas** entre os municípios do Alto Paranaíba – MG, utilizando os algoritmos **Ant Colony Optimization (ACO)** e **Algoritmo Genético (GA)** para resolver o problema do caixeiro viajante (TSP).

## 🧠 Algoritmos Implementados

### 🐜 Ant Colony Optimization (ACO)
- Simula o comportamento de formigas para encontrar rotas eficientes.
- Atualização dinâmica de feromônios com base nas melhores soluções.
- Refinamento com algoritmo **2-opt** para evitar rotas subótimas.

### 🧬 Algoritmo Genético (GA)
- Evolui uma população de rotas por meio de seleção por torneio, crossover parcial e mutação.
- Aplicação do refinamento **2-opt** nas melhores rotas.
- Mantém diversidade com elitismo e controle de duplicatas.

---

## 🗺️ Visualização das Rotas

O sistema gera arquivos HTML interativos com **Google Maps** para visualização das três melhores rotas de cada algoritmo, com cores distintas e destaque para a melhor.

---

## 📊 Resultados
Os resultados são salvos nos arquivos:

dados/top3_aco.json

dados/top3_ga.json

Com as 3 melhores rotas otimizadas de cada abordagem, contendo:

Distância total

Tempo estimado de viagem

Custo logístico estimado



