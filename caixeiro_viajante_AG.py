import numpy as np
import matplotlib.pyplot as plt
import random

# Define a matriz de distâncias
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

# parametros
TAM_POPULACAO = 100
NUM_GERACOES = 1000
TX_MUTACAO = 0.02

def gerar_populacao(tamanho, numero_cidades):
    return [random.sample(range(numero_cidades), numero_cidades) for _ in range(tamanho)]

def fitness(individuo):
    fitness = 0
    for i in range(1, len(individuo)):
        fitness += distancias_cidades[individuo[i-1], individuo[i]]
    fitness += distancias_cidades[individuo[-1], individuo[0]]
    return fitness

# seleção por torneio
def selecao(populacao, aptidoes):
    torneio = random.sample(range(len(populacao)), 5)
    return min(torneio, key=lambda x: aptidoes[x])

def crossover(pai, mae):
    tamanho = len(pai)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho
    filho[inicio:fim] = pai[inicio:fim]
    pos = fim
    for gene in mae:
        if gene not in filho:
            if pos == tamanho:
                pos = 0
            filho[pos] = gene
            pos += 1
    return filho

def mutacao(rota):
    if random.random() < TX_MUTACAO:
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]

def algoritmo_genetico():
    numero_cidades = distancias_cidades.shape[0]
    populacao = gerar_populacao(TAM_POPULACAO, numero_cidades)
    melhores_distancias = []

    for geracao in range(NUM_GERACOES):
        aptidoes = [fitness(rota) for rota in populacao]
        melhores_distancias.append(min(aptidoes))

        nova_populacao = []
        
        for _ in range(TAM_POPULACAO // 2):
            pai = populacao[selecao(populacao, aptidoes)]
            mae = populacao[selecao(populacao, aptidoes)]
            filho1 = crossover(pai, mae)
            filho2 = crossover(mae, pai)
            mutacao(filho1)
            mutacao(filho2)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

    melhor_individuo = populacao[np.argmin([fitness(individuo) for individuo in populacao])]
    melhor_individuo_print = [cidade + 1 for cidade in melhor_individuo]
    melhor_distancia = min(melhores_distancias)
    
    return melhor_individuo_print, melhor_distancia, melhores_distancias

melhor_individuo, melhor_distancia, melhores_distancias = algoritmo_genetico()

plt.figure(figsize=(10, 6))
plt.plot(melhores_distancias, label="Melhor Distância")
plt.title("Convergência do Algoritmo Genético para o Problema do Caixeiro Viajante")
plt.suptitle(f"A melhor rota é {melhor_individuo} com a distancia {melhor_distancia}")
plt.xlabel("Geração")
plt.ylabel("Distância")
plt.legend()
plt.grid()
plt.show()
