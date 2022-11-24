
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
        ## verifica se o numero é valido
        valido = False
        ## se o tamanho da lista for igual a 9
        if len(numero) == 9:
            ## cria um range de 0 a 9
            ref = list(range(9))
            valido = True
            ## para cada numero
            for i in numero:
                ## verifica se ele esta fora da lista
                if int(i) not in ref:
                    valido = False
                else: 
                    ## se estiver dentro remove o elemento da lista
                    ref.remove(int(i))
        return valido

    def construirMatriz(self, str):
        ## separa os numero por virgula
        numeros = str.split(",")
        ## verifica se os numeros sao validos
        if self.numeroValido(numeros):
            i=0
            ## constroi a matriz com os numeros validos
            for k in range(3):
                for j in range(3):
                    self.matriz[k][j] = int(numeros[i])
                    i += 1

    def procurarBloco(self, valor):
        ## procura um valor em algum bloco e retorna o indice da matriz
        for k in range(3):
            for j in range(3):
                if self.matriz[k][j] == valor:
                    return (k,j)

    def moverCima(self, zero):
        ## move o zero um bloco acima
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]-1][zero[1]]
        self.matriz[zero[0]-1][zero[1]] = 0

    def moverBaixo(self, zero):
        ## move o zero um bloco abaixo
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]+1][zero[1]]
        self.matriz[zero[0]+1][zero[1]] = 0

    def moverDireita(self, zero):
        ## move o zero um bloco a direita
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]][zero[1]+1]
        self.matriz[zero[0]][zero[1]+1] = 0

    def moverEsquerda(self, zero):
        ## move o zero um bloco a esquerda
        self.matriz[zero[0]][zero[1]] = self.matriz[zero[0]][zero[1]-1]
        self.matriz[zero[0]][zero[1]-1] = 0

    def getNosPossiveis(self, movimentos):
        ## procura o bloco zero
        zero = self.procurarBloco(0)
        ## cria a lista de posicoes possiveis na qual pode-se movimentar
        nosPossiveis = []
        ## verifica se pode se movimentar para cima
        if zero[0] > 0:
            self.moverCima(zero)
            movimentos.append("cima")
            nosPossiveis.append(deepcopy(self))
            ## passa o zero pra baixo
            zero = self.procurarBloco(0)
            self.moverBaixo(zero)
            zero = self.procurarBloco(0)

        ## verifica se pode se movimentar para baixo
        if zero[0] < 2:
            self.moverBaixo(zero)
            movimentos.append("baixo")
            nosPossiveis.append(deepcopy(self))
            ## pasa o zero para cima
            zero = self.procurarBloco(0)
            self.moverCima(zero)
            zero = self.procurarBloco(0)

        ## verifica se é possível mover para a esquerda
        if zero[1] > 0:
            self.moverEsquerda(zero)
            movimentos.append("esquerda")
            nosPossiveis.append(deepcopy(self))
            ## para o zero para a direita
            zero = self.procurarBloco(0)
            self.moverDireita(zero)
            zero = self.procurarBloco(0)

        if zero[1] < 2:
            ## verifica se é possivel mover para a direita
            self.moverDireita(zero)
            movimentos.append("direita")
            nosPossiveis.append(deepcopy(self))
            ## para o zero para a esquerda
            zero = self.procurarBloco(0)
            self.moverEsquerda(zero)
            zero = self.procurarBloco(0)

        ## retorna as posicoes possiveis
        return nosPossiveis

    def getXY(self, valor, matrizFinal = [[1,2,3],[4,5,6],[7,8,0]]):
        ## retorna os indices de um valor na matriz final
        for x in range(3):
            for y in range(3):
                if valor == matrizFinal[x][y]:
                    return (x,y)
    
    def distanciaManhattan(self):
        res = 0
        ## para cada elemtno da matriz
        for i in range(3):
            for j in range(3):
                ## verifica se o elemento é diferente de zero
                if self.matriz[i][j] != 0:
                    ## retorna os indices do fi e fj da matriz
                    fi, fj = self.getXY(self.matriz[i][j])
                    ## calcula a distancia entre ij e fifj
                    res += abs(fi - i) + abs(fj - j)
        self.distancia = res
        ## retorna a distancia
        return res
    

    def CustoDistanciaManhattan(self, Final):
        res = 0
        ## para cada elemento da matriz
        for i in range(3):
            for j in range(3):
                ## verifica se não é o elemento zero
                if self.matriz[i][j] != 0:
                    ## pega os indices fi fj da matriz final
                    fi, fj = self.getXY(self.matriz[i][j], Final.matriz)
                    ## calcula a distancia entre ij e fifj
                    res += abs(fi - i) + abs(fj - j)
        return res

    def getMatriz(self):
        ## retorna matriz
        return self.matriz

    def eIgual(self, matriz):
        ## verifica se uma matriz é igual a outra
        return (self.matriz == matriz).all()

    def setAnterior(self, a):
        ## set na matriz anterior
        self.anterior = a

    def __cmp__(self, outro):
        ## faz comparação igual
        return self.distancia == outro.distancia
        
    def __lt__(self, outro):
        ## faz comparação menor
        return self.distancia < outro.distancia


