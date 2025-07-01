import json
import os
import webbrowser

API_KEY = "SUA_CHAVE"

base_dir = os.path.dirname(os.path.abspath(__file__))
visualizacao_dir = base_dir
dados_dir = os.path.abspath(os.path.join(base_dir, "..", "dados"))

with open(os.path.join(dados_dir, "top3_ga.json"), "r", encoding="utf-8") as f:
    dados = json.load(f)
    rotas = [r["rota"] for r in dados]
    metricas = [
        f"{r['distancia_km']:.2f} km, {r['tempo_estimado_horas']:.2f} h, R$ {r['custo_estimado_reais']:.2f}"
        for r in dados
    ]

with open(os.path.join(dados_dir, "coordenadas_cidades.json"), "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

cores = ["#FF0000", "#0000FF", "#00AA00"]
nomes = ["GA Rota 1", "GA Rota 2", "GA Rota 3"]

def gerar_html(nome_arquivo, rotas_exibir, legenda_rotas, metricas_exibir, deslocar=True):
    html_path = os.path.join(visualizacao_dir, nome_arquivo)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{nome_arquivo}</title>
    <script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}"></script>
    <style>
        #map {{
            height: 100vh;
            width: 100%;
        }}
        .legenda {{
            position: absolute;
            background-color: white;
            padding: 10px;
            top: 10px;
            left: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="legenda">
        <b>Legenda:</b><br>""")
        for idx, nome in enumerate(legenda_rotas):
            cor = cores[idx % len(cores)]
            f.write(f'<span style="color:{cor};">■</span> {nome}<br>')
            f.write(f'&nbsp;&nbsp;&nbsp;&nbsp;{metricas_exibir[idx]}<br>')
        f.write("""</div>
    <script>
        function initMap() {
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 8,
                center: { lat: -18.9, lng: -46.99 }
            });

            var rotas = """ + json.dumps(rotas_exibir) + """;
            var coordenadas = """ + json.dumps(coordenadas) + """;
            var cores = """ + json.dumps(cores) + """;

            rotas.forEach(function(rota, idx) {
                var path = [];
                rota.forEach(function(cidade, ordem) {
                    var coord = coordenadas[cidade];
                    if (coord) {
                        var lat = coord.lat;
                        var lng = coord.lng;
                        if (""" + str(deslocar).lower() + """) {
                            if (idx === 1) lat += 0.04;
                            if (idx === 2) {{ lat += 0.08; lng += 0.05; }}
                        }
                        path.push({ lat: lat, lng: lng });
                        new google.maps.Marker({
                            position: { lat: lat, lng: lng },
                            map: map,
                            label: {
                                text: (ordem + 1).toString(),
                                fontSize: "11px",
                                fontWeight: "bold"
                            },
                            title: cidade
                        });
                    }
                });

                var polyline = new google.maps.Polyline({
                    path: path,
                    geodesic: true,
                    strokeColor: cores[idx % cores.length],
                    strokeOpacity: 1.0,
                    strokeWeight: 4
                });
                polyline.setMap(map);
            });
        }
        window.onload = initMap;
    </script>
</body>
</html>""")

    print(f"Mapa salvo: {html_path}")
    webbrowser.open(f"file://{html_path}")


gerar_html("mapa_rotas_ga.html", rotas, nomes, metricas)


for i in range(3):
    gerar_html(f"mapa_rota_ga_{i+1}.html", [rotas[i]], [nomes[i]], [metricas[i]], deslocar=False)
