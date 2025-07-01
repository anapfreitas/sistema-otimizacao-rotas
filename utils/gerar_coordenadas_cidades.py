import json
from geopy.geocoders import Nominatim
import time
from dados.lista_cidades import cidades

geolocator = Nominatim(user_agent="geoAnaPaula")
coordenadas = {}

for cidade in cidades:
    try:
        local = geolocator.geocode(f"{cidade}, Minas Gerais, Brasil")
        if local:
            coordenadas[cidade] = [local.latitude, local.longitude]
            print(f"{cidade}: {local.latitude}, {local.longitude}")
        else:
            print(f"Não encontrado: {cidade}")
        time.sleep(1.5)  
    except Exception as e:
        print(f"Erro em {cidade}: {e}")

with open("dados/coordenadas_cidades.json", "w", encoding="utf-8") as f:
    json.dump(coordenadas, f, ensure_ascii=False, indent=2)

print("coordenadas_cidades.json gerado com sucesso.")
