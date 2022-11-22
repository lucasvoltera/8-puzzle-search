
from random import randint
from copy import deepcopy
import numpy as np

class Matriz:
    def __init__(self, linha, coluna):
        self.matriz = np.zeros((linha,coluna), dtype=int)
        self.distancia = 0
        self.anterior = None
        self.movimento = ""
        self.custo = 0
    
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

    def construirMatriz(self, str):
        numeros = str.split(",")
        if self.numeroValido(numeros):
            i=0
            for k in range(3):
                for j in range(3):
                    self.matriz[k][j] = int(numeros[i])
                    i += 1

    def procurarBloco(self, valor):
        for k in range(3):
            for j in range(3):
                if self.matriz[k][j] == valor:
                    return (k,j)

    def moverCima(self, zero):
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]-1][zero[1]]
        self.matriz[zero[0]-1][zero[1]] = 0

    def moverBaixo(self, zero):
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]+1][zero[1]]
        self.matriz[zero[0]+1][zero[1]] = 0

    def moverDireita(self, zero):
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]][zero[1]+1]
        self.matriz[zero[0]][zero[1]+1] = 0

    def moverEsquerda(self, zero):
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]][zero[1]-1]
        self.matriz[zero[0]][zero[1]-1] = 0

    def getNosPossiveis(self, movimentos):
        zero = self.procurarBloco(0)
        nosPossiveis = []

        if zero[0] > 0:
            self.moverCima(zero)
            movimentos.append("up")
            nosPossiveis.append(deepcopy(self))
            zero = self.procurarBloco(0)
            self.moverBaixo(zero)
            zero = self.procurarBloco(0)

        if zero[0] < 2:
            self.moverBaixo(zero)
            movimentos.append("down")
            nosPossiveis.append(deepcopy(self))
            zero = self.procurarBloco(0)
            self.moverCima(zero)
            zero = self.procurarBloco(0)

        if zero[1] > 0:
            self.moverEsquerda(zero)
            movimentos.append("left")
            nosPossiveis.append(deepcopy(self))
            zero = self.procurarBloco(0)
            self.moverDireita(zero)
            zero = self.procurarBloco(0)

        if zero[1] < 2:
            self.moverDireita(zero)
            movimentos.append("right")
            nosPossiveis.append(deepcopy(self))
            zero = self.procurarBloco(0)
            self.moverEsquerda(zero)
            zero = self.procurarBloco(0)

        return nosPossiveis

    def getXY(self, valor, matrizFinal = [[1,2,3],[4,5,6],[7,8,0]]):
        for x in range(3):
            for y in range(3):
                if valor == matrizFinal[x][y]:
                    return (x,y)

    
    def distanciaManhattan(self):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] != 0:
                    fi, fj = self.getXY(self.matriz[i][j])
                    res += abs(fi - i) + abs(fj - j)
        self.distancia = res
        return res
    
    def CustoDistanciaManhattan(self, Final):
        res = 0
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] != 0:
                    fi, fj = self.getXY(self.matriz[i][j], Final.matrix)
                    res += abs(fi - i) + abs(fj - j)
        return res

    def getMatriz(self):
        return self.matriz

    def eIgual(self, matriz):
        return (self.matriz == matriz).all()

    def setAnterior(self, p):
        self.anterior = p

    def __cmp__(self, outro):
        return self.distancia == outro.distancia
        
    def __lt__(self, outro):
        return self.distancia < outro.distancia


