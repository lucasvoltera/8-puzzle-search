from random import randint
from .matriz import Matriz
from queue import PriorityQueue, Queue
import random
import pygame
from utils import *
import numpy as np
import time

class Puzzle:
    def __init__(self, x, y, largura, altura, tempoUltimoResolvido, movimento, cost, matriz,  blocos = [], estadoFinal = "1,2,3,4,5,6,7,8,0"):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.tempoUltimoResolvido = tempoUltimoResolvido ## lastSolveTime
        self.movimento = movimento
        self.custo = cost
        self.matriz = matriz
        self.blocos = blocos
        self.estadoFinal = estadoFinal

    @staticmethod
    def new(x, y, largura, altura):
        return Puzzle(x, y, largura, altura, 0, [], 0, Matriz(3,3), [])

    def numeroValido(self, numero):
        valido = False
        if len(numero) == 9:
            ref = list(range(9))
            valido = True
            for i in numero:
                if int(i) not in ref:
                    valido = False
                else: 
                    ref.remove(int(i))
        return valido
    
    def blocosAleatorios(self): 
        n = randint(30,40)
        for i in range(n):
            zero = self.matriz.procurarBloco(0)
            movimentosPossiveis = []
            #move up
            if zero[0] > 0:
                movimentosPossiveis.append(self.matriz.moverCima)
            if zero[0] < 2:
                movimentosPossiveis.append(self.matriz.moverBaixo)
            if zero[1] > 0:
                movimentosPossiveis.append(self.matriz.moverEsquerda)
            if zero[1] < 2:
                movimentosPossiveis.append(self.matriz.moverDireita)
            random.choice(movimentosPossiveis)(zero)
        self.setBlocosMatriz()

    def setBlocosMatriz(self):
        blocos = []
        bloco_x = self.x
        bloco_y = self.y
        bloco_w = self.largura/ 3
        bloco_h = self.altura / 3
        m = self.matriz.getMatriz()

        i=0
        for k in range(3):
            for j in range(3):
                blocos.append({'rect':pygame.Rect(bloco_x, bloco_y, bloco_w, bloco_h),'color':BABY_BLUE,'block':m[k][j]})
                bloco_x += bloco_w + 1 
                i += 1
            bloco_y += bloco_h + 1
            bloco_x = self.x
        self.blocos = blocos

    def setBlocos(self, string):
        numeros = string.split(",")
        blocos = []
        if self.numeroValido(numeros) :
            bloco_x = self.x
            bloco_y = self.y

            bloco_w = self.largura / 3
            bloco_h = self.altura / 3
            self.matriz.construirMatriz(string)
            i = 0
            for k in range(3):
                for j in range(3):
                    blocos.append({'rect':pygame.Rect(bloco_x, bloco_y, bloco_w, bloco_h),'color':BABY_BLUE,'block':int(numeros[i])})
                    bloco_x += bloco_w + 1 #right
                    i += 1
                bloco_y += bloco_h + 1 #down
                bloco_x = self.x
            self.blocos = blocos
            return True
        return False

    def inicializar(self):
        blocos = self.estadoFinal
        self.setBlocos(blocos)

    def existeEm(self, elem, lista = []):
        for item in lista:
            if item.eIgual(elem):
                return True
        return False

    def getCusto(self, atual):
        while(atual > 0):
            return 1

    ## precisa na real do Breadth first search
    def bestFirst(self):
        #função de avaliação por busca em largura
        inicio = time.time()
        no = self.matriz
        Mfinal = Matriz(3,3)
        Mfinal.construirMatriz(self.estadoFinal) #1,2,3,4,5,6,7,8,0
        final = Mfinal.getMatriz()
        fila = PriorityQueue()
        fila.put(no)
        nosVisitados = []
        n = 1
        
        while(not no.eIgual(final) and not fila.empty()):
            no = fila.get()
            nosVisitados.append(no)
            movimentos = []
            nosFilhos = no.getNosPossiveis(movimentos)
            for i in range(len(nosFilhos)):
                if not self.existeEm(nosFilhos[i].getMatriz(),nosVisitados):
                    nosFilhos[i].movimento = movimentos[i]
                    nosFilhos[i].distanciaManhattan()
                    nosFilhos[i].setAnterior(no)
                    fila._put(nosFilhos[i])
            n += 1
        movimentos = []
        self.custo = n
        if(no.eIgual(final)):
            movimentos.append(no.movimento)
            nd = no.anterior
            while nd != None:
                if nd.movimento != '':
                    movimentos.append(nd.movimento)
                nd = nd.anterior
        fim = time.time()
        self.tempoUltimoResolvido = fim-inicio

        print("## Best-First ##\n")
        print("Tempo gasto {temp: .5f}:".format(temp = fim-inicio))
        print("Nós visitados:",n,"\n")
        return movimentos[::-1]
    
    def a_star(self):
        # iniciando timer
        inicio = time.time()
        no = self.matriz
        Mfinal = Matriz(3,3)
        Mfinal.construirMatriz(self.estadoFinal) #1,2,3,4,5,6,7,8,0
        final = Mfinal.getMatriz()
        fila = PriorityQueue()
        fila.put(no)
        nosVisitados = []
        indicesSelecionados = 0
        n = 1        
        while (not no.eIgual(final) and not fila.empty()):
            no = fila.get()
            nosVisitados.append(no)
            movimentos = []
            nosFilhos = no.getNosPossiveis(movimentos)
            for i in range(len(nosFilhos)):
                if not self.existeEm(nosFilhos[i].getMatriz(), nosVisitados):
                    nosFilhos[i].movimento = movimentos[i]
                    nosFilhos[i].distanciaManhattan()
                    nosFilhos[i].setAnterior(no)
                    # Cumulating the cost function
                    nosFilhos[i].custo = no.cost + no.CustoDistanciaManhattan(nosFilhos[i])
                    nosFilhos[i].distancia += nosFilhos[i].cost
                    fila._put(nosFilhos[i])
            n += 1
            auxCusto = 0
            
        movimentos = []
        self.custo = n
        if(no.eIgual(final)):
            movimentos.append(no.movimento)
            nd = no.anterior
            while nd != None:
                if nd.movimento != '':
                    movimentos.append(nd.movimento)
                nd = nd.anterior
                
        fim = time.time()
        self.tempoUltimoResolvido = fim-inicio
        print("## A* ##\n")
        print("Tempo gasto {temp: .5f}:".format(temp = fim-inicio))
        print("Nós visitados:",n,"\n")
        
        return movimentos[::-1]