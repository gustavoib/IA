import numpy as np
import matplotlib.pyplot as plt
import random

# matriz de distâncias
distancias_cidades = np.array([
    [ 0, 10, 15, 45,  5, 45, 50, 44, 30, 100, 67, 33, 90, 17, 50],
    [15,  0, 100, 30, 20, 25, 80, 45, 41,   5, 45, 10, 90, 10, 35],
    [40, 80,   0, 90, 70, 33, 100, 70, 30,  23, 80, 60, 47, 33, 25],
    [100, 8,   5,  0,  5, 40, 21, 20, 35,  14, 55, 35, 21,  5, 40],
    [17, 10,  33, 45,  0, 14, 50, 27, 33,  60, 17, 10, 20, 13, 71],
    [15, 70,  90, 20, 11,  0, 15, 35, 30,  15, 18, 35, 15, 90, 23],
    [25, 19,  18, 30, 100, 55,  0, 70, 55,  41, 55, 100, 18, 14, 18],
    [40, 15,  60, 45, 70, 33, 25,  0, 27,  60, 80, 35, 30, 41, 35],
    [21, 34,  17, 10, 11, 40,  8, 32,  0,  47, 76, 40, 21, 90, 21],
    [35, 100,  5, 18, 43, 25, 14, 30, 39,   0, 17, 35, 15, 13, 40],
    [38, 20,  23, 30,  5, 55, 50, 33, 70,  14,  0, 60, 30, 35, 21],
    [15, 14,  45, 21, 100, 10,  8, 20, 35,  43,  8,  0, 15, 100, 23],
    [80, 10,   5, 20, 35,  8, 90,  5, 44,  10, 80, 14,  0, 25, 80],
    [33, 90,  40, 18, 70, 45, 25, 23, 90,  44, 43, 70,  5,  0, 25],
    [25, 70,  45, 50,  5, 45, 20, 100, 25,  50, 35, 10, 90,  5,  0]
])

# matriz de distâncias transposta para que a coluna represente a cidade de origem e a linha a cidade de destino
distancias_cidades_transposta = np.transpose(distancias_cidades)

'''
os parametros ALPHA, BETA, RHO, Q e MAX_ITERACOES são hiperparâmetros do algoritmo ACO
- ALPHA: Importância relativa dos feromônios
- BETA: Importância relativa da visibilidade
- RHO: Taxa de evaporação dos feromônios
- Q: Constante para depósito de feromônio
- MAX_ITERACOES: Número máximo de iterações do algoritmo
'''

N_FORMIGAS = 100        
ALPHA = 1.0             
BETA = 2.0              
RHO = 0.5               
Q = 100                 
MAX_ITERACOES = 500     


def inicializar_aco(distancias):
    n_cidades = distancias.shape[0]
    feromonios = np.ones((n_cidades, n_cidades)) / n_cidades
    visibilidade = 1 / (distancias + np.eye(n_cidades))  # evita divisão por zero
    np.fill_diagonal(visibilidade, 0)
    return feromonios, visibilidade

def construir_caminho(feromonios, visibilidade, alpha, beta, n_cidades):
    caminho = [random.randint(0, n_cidades - 1)]  # cidade inicial aleatória
    while len(caminho) < n_cidades:
        cidade_atual = caminho[-1]
        probabilidades = calcular_probabilidades(cidade_atual, caminho, feromonios, visibilidade, alpha, beta)
        proxima_cidade = random.choices(range(n_cidades), weights=probabilidades, k=1)[0]
        caminho.append(proxima_cidade)
    return caminho

def calcular_probabilidades(cidade_atual, caminho, feromonios, visibilidade, alpha, beta):
    n_cidades = feromonios.shape[0]
    probabilidades = np.zeros(n_cidades)
    for j in range(n_cidades):
        if j not in caminho:
            probabilidades[j] = (feromonios[cidade_atual, j] ** alpha) * (visibilidade[cidade_atual, j] ** beta)
    return probabilidades / probabilidades.sum()

def calcular_custo(caminho, distancias):
    custo = 0
    for i in range(len(caminho) - 1):
        custo += distancias[caminho[i], caminho[i + 1]]
    custo += distancias[caminho[-1], caminho[0]]  # retorno à cidade inicial
    return custo

def atualizar_feromonios(feromonios, caminhos, custos, rho, Q):
    n_cidades = feromonios.shape[0]
    delta_feromonios = np.zeros((n_cidades, n_cidades))

    for caminho, custo in zip(caminhos, custos):
        for i in range(len(caminho) - 1):
            delta_feromonios[caminho[i], caminho[i + 1]] += Q / custo
        delta_feromonios[caminho[-1], caminho[0]] += Q / custo  # fechamento do ciclo

    feromonios *= (1 - rho)
    feromonios += delta_feromonios

def algoritmo_colonia_de_formigas(distancias):
    n_cidades = distancias.shape[0]
    feromonios, visibilidade = inicializar_aco(distancias)

    melhor_caminho = None
    melhor_custo = float('inf')
    melhores_custos = []

    for iteracao in range(MAX_ITERACOES):
        caminhos = []
        custos = []

        for _ in range(N_FORMIGAS):
            caminho = construir_caminho(feromonios, visibilidade, ALPHA, BETA, n_cidades)
            custo = calcular_custo(caminho, distancias)

            caminhos.append(caminho)
            custos.append(custo)

            if custo < melhor_custo:
                melhor_caminho = caminho
                melhor_custo = custo

        atualizar_feromonios(feromonios, caminhos, custos, RHO, Q)
        melhores_custos.append(melhor_custo)
        
        melhor_caminho_print = [cidade + 1 for cidade in melhor_caminho]

        # print(f"Iteração {iteracao + 1}/{MAX_ITERACOES}: Melhor custo = {melhor_custo}")

    return melhor_caminho_print, melhor_custo, melhores_custos


# execução do algoritmo
melhor_caminho, melhor_custo, melhores_custos = algoritmo_colonia_de_formigas(distancias_cidades_transposta)

print(f"Melhor caminho: {melhor_caminho}")
print(f"Custo do melhor caminho: {melhor_custo}")

# Plotar a convergência
plt.figure(figsize=(10, 6))
plt.plot(melhores_custos, label="Melhor Custo")
plt.title("Convergência do Algoritmo de Colônia de Formigas para o Problema do Caixeiro Viajante")
plt.suptitle(f"A melhor rota é {melhor_caminho} com o custo {melhor_custo}")
plt.xlabel("Iteração")
plt.ylabel("Custo")
plt.legend()
plt.grid()
plt.show()