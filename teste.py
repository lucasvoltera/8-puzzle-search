## precisa na real do Breadth first search
def bestFirst(self):
    #inicio do tempo
    inicio = time.time()

    ## no recebe a matriz
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
            if not self.existeEm(nosFilhos[i].getMatriz(),nosVisitados):
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

    print("## Best-First ##\n")
    print("Tempo gasto {temp: .5f}:".format(temp = fim-inicio))
    print("Nós visitados:",n,"\n")
    return movimentos[::-1]



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

