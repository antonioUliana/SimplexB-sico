from __future__ import division
from numpy import *


class Simplex:
    #Definindo a equacao que vai ser calculada o max: z - 5x1 - 4x2 - 3x3
    def __init__(self, objetivo):
        self.objetivo = [1] + objetivo
        self.linhas = []
        self.const = [] #coluna de constantes


    #adiciona as restrições iniciais na tabela
    #limite é o valor que limita a expressao ( vem depois do <= )
    def restricao(self, equacao, limite):
        self.linhas.append([0] + equacao)
        self.const.append(limite)

    #coluna pivo tem que ser o indice mais negativo
    def coluna_pivo(self):
        menor_indice = 0
        pos = 0 #posicao do menor indice na matriz
        for i in range(1, len(self.objetivo) - 1):
            if self.objetivo[i] < menor_indice:
                menor_indice = self.objetivo[i]
                pos = i
        if pos == 0: return -1 #se nao encontrar valor negativo, o valor max ja foi encontrado
        return pos

    def linha_pivo(self, coluna):
        #coloca os valores da coluna de constantes num vetor
        col_const = [i[-1] for i in self.linhas]
        # coloca os valores da coluna pivo num vetor
        col_pivo = [i[coluna] for i in self.linhas]

        fracoes = []
        for i in range(len(col_const)):
            if col_pivo[i] == 0:
                #se o valor do denominador for zero, entao coloca um numero que tende a infinito
                fracoes.append(99999999.0)
            else:
                fracoes.append(col_const[i] / col_pivo[i])
        #argmin é uma propriedade da bibilioteca numpy que encontra o index de menor valor do vetor
        return argmin(fracoes)


    def imprime(self):
        print('\n', matrix([self.objetivo] + self.linhas))
        print('\n', 'O valor de Z até agora é', self.objetivo[len(self.objetivo)-1])

    def pivo(self, linha, coluna):
        elemento_pivo = self.linhas[linha][coluna]
        print('\n','pivô:', elemento_pivo)
        print('','linha pivô:', linha+2)
        print('','coluna pivô:', coluna+1)
        self.linhas[linha] /= elemento_pivo
        for cada_linha in range(len(self.linhas)):
            if cada_linha != linha: #ignora a linha pivo
                self.linhas[cada_linha] = self.linhas[cada_linha] - self.linhas[cada_linha][coluna] * self.linhas[linha]
        self.objetivo = self.objetivo - self.objetivo[coluna] * self.linhas[linha]


    def verifica_maximizacao(self):
        for i in range(len(self.linhas)):
            if min(self.objetivo) >= 0:
                print('\n', 'Z foi maximizado')
                return 1
        return 0

    def solucao(self):

        #construção da tabela do simplex
        for i in range(len(self.linhas)):
            # acrescenta as variaveis basicas na tabela
            self.objetivo += [0]
            variaveis_basicas = [0 for linha in range(len(self.linhas))]
            variaveis_basicas[i] = 1
            self.linhas[i] += variaveis_basicas + [self.const[i]]
            self.linhas[i] = array(self.linhas[i], dtype=float)
        self.objetivo = array(self.objetivo + [0], dtype=float)

        #linha pivo sai da base, coluna pivo entra na base
        self.imprime()
        while not self.verifica_maximizacao():
            c = self.coluna_pivo()
            r = self.linha_pivo(c)
            print('\n', 'linha x', r+len(self.linhas)+1, '=', 'coluna x', c)
            self.pivo(r, c)
            self.imprime()


if __name__ == '__main__':

    """
    max Z = 5x1 + 4x2 + 3x3 s.r.

    2x1 + 3x2 + x3 <= 5
    4x1 + 2x2 + 2x3 <= 11
    3x1 + 2x2 + 2x3 <= 8
    x1,x2,x3 >= 0
    Sol: x1 = 2; x2 = 0; x3 = 1; x4 = 0; x5 = 1; x6 = 0 e Z = 13

    """

    t = Simplex([-5, -4, -3])
    t.restricao([2, 3, 1], 5)
    t.restricao([4, 2, 2], 11)
    t.restricao([3, 2, 2], 8)
    t.solucao()