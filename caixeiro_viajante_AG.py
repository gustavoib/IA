import numpy as np

# matriz com as distacias para cada cidade
distancias_cidades = np.array([
    [  0,  10,  15,  45,   5,  45,  50,  44,  30, 100,  67,  33,  90,  17,  50],
    [ 15,   0, 100,  30,  20,  25,  80,  45,  41,   5,  45,  10,  90,  10,  35],
    [ 40,  80,   0,  90,  70,  33, 100,  70,  30,  23,  80,  60,  47,  33,  25],
    [100,   8,   5,   0,   5,  40,  21,  20,  35,  14,  55,  35,  21,   5,  40],
    [ 17,  10,  33,  45,   0,  14,  50,  27,  33,  60,  17,  10,  20,  13,  71],
    [ 15,  70,  90,  20,  11,   0,  15,  35,  30,  15,  18,  35,  15,  90,  23],
    [ 25,  19,  18,  30, 100,  55,   0,  70,  55,  41,  55, 100,  18,  14,  18],
    [ 40,  15,  60,  45,  70,  33,  25,   0,  27,  60,  80,  35,  30,  41,  35],
    [ 21,  34,  17,  10,  11,  40,   8,  32,   0,  47,  76,  40,  21,  90,  21],
    [ 35, 100,   5,  18,  43,  25,  14,  30,  39,   0,  17,  35,  15,  13,  40],
    [ 38,  20,  23,  30,   5,  55,  50,  33,  70,  14,   0,  60,  30,  35,  21],
    [ 15,  14,  45,  21, 100,  10,   8,  20,  35,  43,   8,   0,  15, 100,  23],
    [ 80,  10,   5,  20,  35,   8,  90,   5,  44,  10,  80,  14,   0,  25,  80],
    [ 33,  90,  40,  18,  70,  45,  25,  23,  90,  44,  43,  70,   5,   0,  25],
    [ 25,  70,  45,  50,   5,  45,  20, 100,  25,  50,  35,  10,  90,   5,   0],
])

'''
Obs: 
- cada gene representa uma cidade;
- cada individuo é uma sequencia de cidades;
- a populacao é um conjunto de individuos;
'''

# funcao de fitness - distancia total percorrida 
def fitness(individuo):
    fitness = 0
    for i in range(1, len(individuo)):
        fitness += distancias_cidades[individuo[i-1], individuo[i]]
    fitness += distancias_cidades[individuo[-1], individuo[0]]
    return fitness

# função que gerar uma nova população com base na quantidade de individuos e genes
def nova_populacao(qtd_individuos, qtd_genes):
    populacao = np.zeros((qtd_individuos, qtd_genes), dtype=int)
    for i in range(qtd_individuos):
        populacao[i] = np.random.permutation(qtd_genes)
    return populacao

# função que seleciona os individuos com base no fitness - metodo da roleta
def selecao_aleatoria(populacao):
    fitness_populacao = np.array([fitness(individuo) for individuo in populacao])
    return populacao[np.argsort(fitness_populacao)]

# função que realiza a mutação - troca a posição de dois genes se a probabilidade for menor que a taxa de mutação
def mutacao(individuo, taxa_mutacao):
    # a partir de uma pequena probabilidade, troca a posicao de dois genes
    if np.random.rand() < taxa_mutacao:
        i, j = np.random.choice(len(individuo), 2, replace=False)
        individuo[i], individuo[j] = individuo[j], individuo[i]

# função que realiza o cruzamento - pega parte do pai e parte da mãe para formar o filho
def cruzamento(pai, mae):
    n = len(pai)
    local_cruzamento = np.random.randint(n)
    corte_pai = pai[local_cruzamento:]
    corte_mae = [gene for gene in mae if gene not in corte_pai]
    filho = np.array(np.concatenate((corte_pai, corte_mae)), dtype=int)
    return filho

# função principal - algoritmo genético para o problema do caixeiro viajante
def caixeiro_viajante_AG(qtd_individuos, qtd_genes, taxa_mutacao, qtd_geracoes):
    populacao = nova_populacao(qtd_individuos, qtd_genes)
    
    # inicializa a populacao com individuos aleatorios e calcula o fitness de cada individuo
    for i in range(len(populacao)):
        pai = selecao_aleatoria(populacao)
        mae = selecao_aleatoria(populacao)
        filho = cruzamento(pai[0], mae[0])
        mutacao(filho, taxa_mutacao)
        populacao[i] = filho.copy()
        
    melhor_fitness = np.inf
    melhor_individuo = None
    
    # para cada geracao, seleciona os individuos, realiza o cruzamento e a mutacao
    for i in range(qtd_geracoes):
        populacao = selecao_aleatoria(populacao)
        
        for i in range(0, len(populacao), 2):
            pai = populacao[i]
            mae = populacao[i+1]
            filho = cruzamento(pai, mae)
            mutacao(filho, taxa_mutacao)
            populacao[i] = filho.copy()
        
        if fitness(populacao[0]) < melhor_fitness:
            melhor_fitness = fitness(populacao[0])
            melhor_individuo = populacao[0]
            
    return melhor_individuo + 1, melhor_fitness
        
# Teste
qtd_individuos = 100
qtd_genes = 15
taxa_mutacao = 0.002
qtd_geracoes = 1000

melhor_individuo, melhor_fitness = caixeiro_viajante_AG(qtd_individuos, qtd_genes, taxa_mutacao, qtd_geracoes)

print('Melhor individuo:', melhor_individuo)
print('Melhor fitness:', melhor_fitness)