import random
import math
from typing import List, Tuple
import re
import matplotlib.pyplot as plt

class Experimentos:
    def __init__(self, n_pop: int, coordinates: List[Tuple[float, float]], taxa_crossover: float):
        self.n_pop = n_pop  # Tamanho da população
        self.coordinates = coordinates  # Coordenadas das cidades
        self.taxa_crossover = taxa_crossover  # Taxa de crossover
        self.n_genes = len(coordinates)  # Número de genes (cidades)
        self.pop = []  # População inicial
        self.fitness = []  # Lista para armazenar o fitness de cada indivíduo
        self.melhor_global = None  # Melhor indivíduo global
        self.melhor_custo_global = float('inf')  # Inicializa com um valor infinito


    def inicializar_populacao(self):
        """Inicializa a população com rotas aleatórias"""
        for _ in range(self.n_pop):
            rota = [i for i in range(self.n_genes)]
            random.shuffle(rota)
            self.pop.append(rota)

    def calcular_distancia_entre_cidades(self, cidade1: int, cidade2: int) -> float:
        """Calcula a distância euclidiana entre duas cidades"""
        x1, y1 = self.coordinates[cidade1]
        x2, y2 = self.coordinates[cidade2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calcular_fitness(self, rota: List[int]) -> float:
        """Calcula o fitness (distância total da rota) para uma rota"""
        distancia_total = 0.0
        for i in range(self.n_genes - 1):
            cidade_atual = rota[i]
            proxima_cidade = rota[i + 1]
            distancia_total += self.calcular_distancia_entre_cidades(cidade_atual, proxima_cidade)
        distancia_total += self.calcular_distancia_entre_cidades(rota[-1], rota[0])
        return distancia_total

    def selecionar_pais(self) -> List[List[int]]:
        """Seleciona os pais via torneio"""
        pais = []
        for _ in range(self.n_pop):
            idx_1 = random.randint(0, self.n_pop - 1)
            idx_2 = random.randint(0, self.n_pop - 1)
            pai = self.pop[idx_1] if self.fitness[idx_1] < self.fitness[idx_2] else self.pop[idx_2]
            pais.append(pai)
        return pais

    def crossover(self, pais: List[List[int]]) -> List[List[int]]:
        """Realiza o crossover dos pais para gerar filhos"""
        filhos = []
        for i in range(0, self.n_pop, 2):
            pai_1 = pais[i]
            pai_2 = pais[i + 1]
            if random.random() < self.taxa_crossover:  # Verifica a taxa de crossover
                ponto_corte = random.randint(1, self.n_genes - 1)
                filho_1 = pai_1[:ponto_corte] + [gene for gene in pai_2 if gene not in pai_1[:ponto_corte]]
                filho_2 = pai_2[:ponto_corte] + [gene for gene in pai_1 if gene not in pai_2[:ponto_corte]]
                filhos.extend([filho_1, filho_2])
            else:
                filhos.extend([pai_1, pai_2])  # Não houve crossover
        return filhos

    def mutacao(self, filhos: List[List[int]], taxa_mutacao: float):
        """Aplica mutação aos filhos"""
        for i in range(len(filhos)):
            if random.random() < taxa_mutacao:
                idx_1 = random.randint(0, self.n_genes - 1)
                idx_2 = random.randint(0, self.n_genes - 1)
                filhos[i][idx_1], filhos[i][idx_2] = filhos[i][idx_2], filhos[i][idx_1]
                
    
    def selecao_sobreviventes(self, filhos: List[List[int]]):
        """Seleciona os sobreviventes para a próxima geração"""
        self.pop = filhos

    def executar_experimento(self, taxa_mutacao: float, n_geracoes: int):
        self.inicializar_populacao()
        for geracao in range(n_geracoes):
            self.fitness = [self.calcular_fitness(rota) for rota in self.pop]
            pais = self.selecionar_pais()
            filhos = self.crossover(pais)
            self.mutacao(filhos, taxa_mutacao)
            self.selecao_sobreviventes(filhos)
            melhor_fitness = min(self.fitness)
            melhor_rota_idx = self.fitness.index(melhor_fitness)
            melhor_rota = self.pop[melhor_rota_idx]
            if melhor_fitness < self.melhor_custo_global:
                self.melhor_global = melhor_rota
                self.melhor_custo_global = melhor_fitness
            # print(f"Geração {geracao + 1} - Melhor Rota Atual: {melhor_rota} - Custo Atual: {melhor_fitness}")

        # Ao final de todas as gerações, mostrar o melhor global
        print("\nMelhor Indivíduo Global:", self.melhor_global)
        print("Custo do Melhor Indivíduo:", self.melhor_custo_global)

def plot_cidades(coordinates, rota=None):
        x = [coord[0] for coord in coordinates]
        y = [coord[1] for coord in coordinates]

        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, marker='o', color='blue', label='Cidades')

        if rota:
            rota_x = [coordinates[i][0] for i in rota]
            rota_y = [coordinates[i][1] for i in rota]
            rota_x.append(coordinates[rota[0]][0])
            rota_y.append(coordinates[rota[0]][1])
            plt.plot(rota_x, rota_y, linestyle='-', marker='o', color='red', label='Melhor Rota')

        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title('Mapa das Cidades')
        plt.legend()
        plt.grid()
        plt.show()


def ler_coordenadas(nome_arquivo: str) -> List[Tuple[float, float]]:
    """Lê as coordenadas das cidades a partir de um arquivo"""
    coordenadas = []
    with open(nome_arquivo, 'r') as arquivo:
        ler_coordenadas = False
        for linha in arquivo:
            if linha.startswith("NODE_COORD_SECTION"):
                ler_coordenadas = True
                continue
            elif linha.startswith("EOF"):
                break
            if ler_coordenadas:
                dados = re.findall(r'\d+\.\d+', linha)
                x = float(dados[0])
                y = float(dados[1])
                coordenadas.append((x, y))
    return coordenadas

if __name__ == "__main__":
    for i in range(10):
        n_pop = 100
        nome_arquivo = "C:/Users/leand/Downloads/berlin52.tsp"  # Substitua pelo nome do seu arquivo
        coordenadas = ler_coordenadas(nome_arquivo)
        taxa_crossover = 0.8072899070477247
        taxa_mutacao = 0.009229974637784487
        n_geracoes = 5161
        experimento = Experimentos(n_pop, coordenadas, taxa_crossover)
        experimento.executar_experimento(taxa_mutacao, n_geracoes)
        
        experimento.executar_experimento(taxa_mutacao, n_geracoes)

        # Plotar as cidades e a melhor rota global
        experimento.melhor_global.append(experimento.melhor_global[0])  # Fechar o ciclo
        plot_cidades(coordenadas, experimento.melhor_global)
    
    