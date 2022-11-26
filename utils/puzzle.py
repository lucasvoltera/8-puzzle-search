from random import randint
from .matriz import Matriz
from queue import PriorityQueue, Queue
import random
import pygame
from utils import *
import numpy as np
import time

class Puzzle:
    def __init__(self, x, y, largura, altura, tempoUltimoResolvido, movimento, custo, matriz,  blocos = [], estadoFinal = "1,2,3,4,5,6,7,8,0"):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.tempoUltimoResolvido = tempoUltimoResolvido
        self.movimento = movimento
        self.custo = custo
        self.matriz = matriz
        self.blocos = blocos
        self.estadoFinal = estadoFinal

    @staticmethod
    def new(x, y, largura, altura):
        ## função que cria um novo puzzle 3x3
        return Puzzle(x, y, largura, altura, 0, [], 0, Matriz(NRO_LINHA,NRO_COLUNA), [])

    def numeroValido(self, numero):
        ### função que verifica se o número é válido ou não
        valido = False
        ## verifica se o tamanho é igual a 9
        if len(numero) == 9:
            ## cria uma lista de 0 a 9
            ref = list(range(9))
            valido = True
            ## para cada numero
            for i in numero:
                ## verifica se o número está contido no range de valores
                if int(i) not in ref:
                    ## se estiver, então ele não é mais válido
                    valido = False
                else: 
                    ## se estiver, então remove ele da lista
                    ref.remove(int(i))
        ## retorna se é valido ou não
        return valido

    def getMovimentosPossiveis(self, zero):
        movimentosPossiveis = []
        ## de acordo com a coordenada, verifica quais são os movimentos possíveis e armazena em uma lista 
        if zero[0] > 0:
            movimentosPossiveis.append(self.matriz.moverCima)
        if zero[0] < 2:
            movimentosPossiveis.append(self.matriz.moverBaixo)
        if zero[1] > 0:
            movimentosPossiveis.append(self.matriz.moverEsquerda)
        if zero[1] < 2:
            movimentosPossiveis.append(self.matriz.moverDireita)
        return movimentosPossiveis

    
    def blocosAleatorios(self): 
        ## pega um valor inteiro aleatório entre 30 a 40
        n = randint(30,40)
        ## para cada valor de 0 a n
        for i in range(n):
            ## procura pelo bloco 0 e retorna a coordenada do bloco zero
            zero = self.matriz.procurarBloco(0)
            movimentosPossiveis = self.getMovimentosPossiveis(zero)
            ## manda para alguma posição aleatória dentra as possiveis
            random.choice(movimentosPossiveis)(zero)
        ## faz a matriz
        self.setBlocosMatriz()

    def setBlocosMatriz(self):
        ## pega algumas informações da matriz
        bloco_x = self.x
        bloco_y = self.y
        bloco_w = self.largura / 3
        bloco_h = self.altura / 3
        ## retorna uma matriz de zeros
        m = self.matriz.getMatriz()
        self.blocos = self.construirBlocos(bloco_x, bloco_y, bloco_w, bloco_h, matriz = m)

    def construirBlocos(self, bloco_x, bloco_y, bloco_w, bloco_h, numeros = None, matriz = None):
        blocos = []
        i = 0
        for k in range(NRO_LINHA):
            for j in range(NRO_COLUNA):
                if numeros == None:
                    ## para cada bloco, armazena as medidas do retangulo, a cor e os indeces do bloco, armazenando tudo em uma lista
                    blocos.append({'rect':pygame.Rect(bloco_x, bloco_y, bloco_w, bloco_h),'color':KINDA_OF_BLACK ,'bloco':matriz[k][j]})
                else:
                    blocos.append({'rect':pygame.Rect(bloco_x, bloco_y, bloco_w, bloco_h),'color':KINDA_OF_BLACK ,'bloco':int(numeros[i])})
                bloco_x += bloco_w + 1 #right
                i += 1
            bloco_y += bloco_h + 1 #down
            bloco_x = self.x
        return blocos



    def setBlocos(self, string):
        ## separa os numeros por virgula
        numeros = string.split(",")
        ## verifica se os numeros são validos
        if self.numeroValido(numeros):
            ## pegando as informações do retangulo
            bloco_x = self.x
            bloco_y = self.y
            bloco_w = self.largura / 3
            bloco_h = self.altura / 3
            ## constroi a matriz com os numeros validados pelo usuario
            self.matriz.construirMatriz(string)
            self.blocos = self.construirBlocos(bloco_x, bloco_y, bloco_w, bloco_h, numeros = numeros)
            return True
        return False

    def inicializar(self):
        ## define quais serão os blocos do estado final
        blocos = self.estadoFinal
        self.setBlocos(blocos)

    def existeEm(self, elem, lista = []):
        ## verifica se um valor esta na lista
        for item in lista:
            if item.eIgual(elem):
                return True
        return False

    def getCusto(self, atual):
        ## verifica o custo da função
        while(atual > 0):
            return 1

    ## best-search
    def heristicaPessoal(self):
        #inicio do tempo
        inicio = time.time()

        ## no recebe a matriz (tabuleiro)
        no = self.matriz
        ## cria uma matriz final 3x3
        Mfinal = Matriz(3,3)
        ## constroi a matriz final de acordo com a variavel estado inicial
        Mfinal.construirMatriz(self.estadoFinal) #1,2,3,4,5,6,7,8,0
        ## copia a matriz final
        final = Mfinal.getMatriz()
        ## cria uma fila de prioridade
        fila = PriorityQueue()
        ## adiciona a matriz na fila
        fila.put(no)
        ## cria uma lista de nos visitados
        nosVisitados = []
        n = 1
        
        ## enquanto o nó não é igual e a fila nnao etiver vazia
        while(not no.eIgual(final) and not fila.empty()):
            ## retira o elemento primeiro elemento da fila
            no = fila.get()
            ## adiciona o no visitado
            nosVisitados.append(no)
            ## cria uma lista de movimentos
            movimentos = []
            ## pega os nos possiveis a serem visitados
            nosFilhos = no.getNosPossiveis(movimentos)
            ## para cada no filho
            for i in range(len(nosFilhos)):
                ## se o nó não está entre os visitados e calcula a distancia, e seta os nós anteriores
                if not self.existeEm(nosFilhos[i].getMatriz(), nosVisitados):
                    nosFilhos[i].movimento = movimentos[i]
                    nosFilhos[i].distanciaManhattan()
                    nosFilhos[i].setAnterior(no)
                    fila._put(nosFilhos[i])
            n += 1
        ## cria a lista de movimentos
        movimentos = []
        self.custo = n
        ## se o nó for igual ao final
        if(no.eIgual(final)):
            ## armazena os movimentos
            movimentos.append(no.movimento)
            ## registra o anterior
            nd = no.anterior
            ## se o nó anterior for diferente de vazio
            while nd != None:
                ## e o movimento for diferente de vazio
                if nd.movimento != '':
                    ## faz armazena o anterior
                    movimentos.append(nd.movimento)
                ## atualiza quem é o anterior
                nd = nd.anterior
        ## para de contar o tempo do algoritmo
        fim = time.time()
        ## calcula o tempo total
        self.tempoUltimoResolvido = fim-inicio

        #print("## Best-First ##\n")
        #print("Tempo gasto {temp: .5f}:".format(temp = fim-inicio))
        #print("Nós visitados:",n,"\n")
        return movimentos[::-1]
    
    ## greedy search
    def heuristica1(self):
        #inicio do tempo
        inicio = time.time()

        ## no recebe a matriz (tabuleiro)
        no = self.matriz
        ## cria uma matriz final 3x3
        Mfinal = Matriz(3,3)
        ## constroi a matriz final de acordo com a variavel estado inicial
        Mfinal.construirMatriz(self.estadoFinal) #1,2,3,4,5,6,7,8,0
        ## copia a matriz final
        final = Mfinal.getMatriz()
        ## cria uma fila de prioridade
        fila = Queue()
        ## adiciona a matriz na fila
        fila.put(no)
        ## cria uma lista de nos visitados
        nosVisitados = []
        n = 1
        
        ## enquanto o nó não é igual e a fila nnao etiver vazia
        while(not no.eIgual(final) and not fila.empty()):
            ## retira o elemento primeiro elemento da fila
            no = fila.get()
            ## adiciona o no visitado
            nosVisitados.append(no)
            ## cria uma lista de movimentos
            movimentos = []
            ## pega os nos possiveis a serem visitados
            nosFilhos = no.getNosPossiveis(movimentos)
            ## para cada no filho
            for i in range(len(nosFilhos)):
                ## se o nó não está entre os visitados e calcula a distancia, e seta os nós anteriores
                if not self.existeEm(nosFilhos[i].getMatriz(), nosVisitados):
                    nosFilhos[i].movimento = movimentos[i]
                    nosFilhos[i].distanciaManhattan()
                    nosFilhos[i].setAnterior(no)
                    fila._put(nosFilhos[i])
            n += 1
        ## cria a lista de movimentos
        movimentos = []
        self.custo = n
        ## se o nó for igual ao final
        if(no.eIgual(final)):
            ## armazena os movimentos
            movimentos.append(no.movimento)
            ## registra o anterior
            nd = no.anterior
            ## se o nó anterior for diferente de vazio
            while nd != None:
                ## e o movimento for diferente de vazio
                if nd.movimento != '':
                    ## faz armazena o anterior
                    movimentos.append(nd.movimento)
                ## atualiza quem é o anterior
                nd = nd.anterior
        ## para de contar o tempo do algoritmo
        fim = time.time()
        ## calcula o tempo total
        self.tempoUltimoResolvido = fim-inicio
        return movimentos[::-1]

    ## adaptacao a* - nivel 2
    def heuristica2(self):
        # iniciando timer
        inicio = time.time()

        ## no recebe a matriz
        no = self.matriz
        ## criando a matriz final 3x3
        Mfinal = Matriz(3,3)
        ## matriz final recebe os elementos do estado final
        Mfinal.construirMatriz(self.estadoFinal) #1,2,3,4,5,6,7,8,0
        ## final recebe a matriz da matriz final
        final = Mfinal.getMatriz()
        ## criando uma fila de prioridade
        fila = PriorityQueue()
        ## pondo o no na fila
        fila.put(no)
        ## criando uma lista dos nos visitados
        nosVisitados = []
        ## variavel dos indices selecionados
        indicesSelecionados = 0
        n = 1        

        ## enquanto o no é diferente de final e a fila nao esta vazia
        while (not no.eIgual(final) and not fila.empty()):
            ## faz um pop na fila
            no = fila.get()
            ## armazena o no em nos visitados
            nosVisitados.append(no)
            movimentos = []
            ## verifica quais são os nos acessiveis
            nosFilhos = no.getNosPossiveis(movimentos)
            ## para cada no acessivel
            for i in range(len(nosFilhos)):
                ## se o no nao esta entre os nos visitados, calcula a distancia e seta o no anterior
                if not self.existeEm(nosFilhos[i].getMatriz(), nosVisitados):
                    nosFilhos[i].movimento = movimentos[i]
                    nosFilhos[i].distanciaManhattan()
                    nosFilhos[i].setAnterior(no)
                    # acumula a função de custo
                    nosFilhos[i].custo = no.custo + no.CustoDistanciaManhattan(nosFilhos[i])
                    nosFilhos[i].distancia += nosFilhos[i].custo
                    fila._put(nosFilhos[i])
            n += 1
            auxCusto = 0
        
        ## cria a lista dos movimentos
        movimentos = []
        self.custo = n
        ## se o no for igual ao final
        if(no.eIgual(final)):
            ## armazena o movimento daquele no 
            movimentos.append(no.movimento)
            ## armazena o anterior daquele no
            nd = no.anterior
            ## enquanto existir um anterior
            while nd != None:
                ## verifica se há um movimento
                if nd.movimento != '':
                    ## armazena o movimento daquele anterior
                    movimentos.append(nd.movimento)
                ## atualiza o anterior
                nd = nd.anterior
        
        ## termina de contar
        fim = time.time()
        ## calcula o tempo
        self.tempoUltimoResolvido = fim-inicio        
        return movimentos[::-1]
