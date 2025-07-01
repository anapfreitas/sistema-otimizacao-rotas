import tkinter as tk
import subprocess
import os

def abrir_mapa_aco(_=None):
    caminho_script = os.path.join("visualizacao", "visualizador_mapa_aco.py")
    arquivo_html = "mapa_rotas_aco.html"
    subprocess.Popen(["python", caminho_script, arquivo_html])

def abrir_mapa_ga(_=None):
    caminho_script = os.path.join("visualizacao", "visualizador_mapa_ga.py")
    arquivo_html = "mapa_rotas_ga.html"
    subprocess.Popen(["python", caminho_script, arquivo_html])

def abrir_tabela_comparativa():
    subprocess.Popen(["python", "interface_tabela_comparativa.py"])

def executar_algoritmo_aco():
    subprocess.run(["python", "algoritmos/algoritmo_aco.py"])

def executar_algoritmo_ga():
    subprocess.run(["python", "algoritmos/algoritmo_genetico.py"])

def abrir_graficos_comparativos():
    caminho_script = os.path.join("visualizacao", "visualizacao_graficos.py")
    subprocess.Popen(["python", caminho_script])

def abrir_grafo_com_pesos():
    caminho_script = os.path.join("visualizacao", "visualizar_grafo_com_pesos.py")
    subprocess.Popen(["python", caminho_script])

def criar_interface_principal():
    janela = tk.Tk()
    janela.title("Otimizador Logístico")
    janela.geometry("500x520")

    tk.Label(janela, text="Otimizador Logístico - ACO e GA", font=("Arial", 16)).pack(pady=10)

    # Execução dos Algoritmos
    tk.Button(janela, text="Executar ACO", command=executar_algoritmo_aco).pack(pady=5)
    tk.Button(janela, text="Executar GA", command=executar_algoritmo_ga).pack(pady=5)

    # Mapas ACO
    tk.Label(janela, text="Abrir Mapas ACO:").pack()
    tk.Button(janela, text="Visualizar 3 Rotas ACO", command=abrir_mapa_aco).pack(pady=5)

    # Mapas GA
    tk.Label(janela, text="Abrir Mapas GA:").pack()
    tk.Button(janela, text="Visualizar 3 Rotas GA", command=abrir_mapa_ga).pack(pady=5)

    # Tabela Comparativa
    tk.Button(janela, text="Abrir Tabela Comparativa", command=abrir_tabela_comparativa).pack(pady=10)

    # Gráficos Comparativos
    tk.Button(janela, text="Ver Gráficos Comparativos", command=abrir_graficos_comparativos).pack(pady=10)

    # Visualização do Grafo com Pesos
    tk.Label(janela, text="Visualização do Grafo com Pesos:").pack(pady=(10, 0))
    tk.Button(janela, text="Ver Grafo com Distância / Tempo / Custo", width=30, command=abrir_grafo_com_pesos).pack(pady=2)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface_principal()
