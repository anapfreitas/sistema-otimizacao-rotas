import tkinter as tk
from tkinter import ttk
import json

def carregar_dados():
    with open("dados/top3_aco.json", "r", encoding="utf-8") as f:
        aco = json.load(f)
    with open("dados/top3_ga.json", "r", encoding="utf-8") as f:
        ga = json.load(f)
    return aco, ga

def mostrar_tabela():
    janela = tk.Tk()
    janela.title("Tabela Comparativa - ACO vs GA")
    janela.geometry("780x300")

    colunas = ("Algoritmo", "Distância (km)", "Tempo (h)", "Custo (R$)")
    tabela = ttk.Treeview(janela, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor=tk.CENTER, width=180)

    aco, ga = carregar_dados()

    for i in range(3):
        aco_dist = round(aco[i].get("distancia_km", 0), 2)
        aco_tempo = round(aco[i].get("tempo_estimado_horas", 0), 2)
        aco_custo = round(aco[i].get("custo_estimado_reais", 0), 2)

        ga_dist = round(ga[i].get("distancia_km", 0), 2)
        ga_tempo = round(ga[i].get("tempo_estimado_horas", 0), 2)
        ga_custo = round(ga[i].get("custo_estimado_reais", 0), 2)

        tabela.insert("", "end", values=(f"ACO Rota {i+1}", f"{aco_dist} km", f"{aco_tempo} h", f"R$ {aco_custo}"))
        tabela.insert("", "end", values=(f"GA Rota {i+1}", f"{ga_dist} km", f"{ga_tempo} h", f"R$ {ga_custo}"))

    tabela.pack(pady=20)
    janela.mainloop()

if __name__ == "__main__":
    mostrar_tabela()
