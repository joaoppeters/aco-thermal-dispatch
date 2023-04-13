


#########################################
# Created by: Joao Pedro Peters Barbosa #
#       & Pedro Henrique Peters Barbosa #
#                                       #
# email: joao.peters@engenharia.ufjf.br #
#  or pedro.henrique@engenharia.ufjf.br #
#########################################


"""
Disciplina [210115] - Topicos Especiais em Otimizacao: Tecnicas Inteligentes

Desenvolvimento do programa referente ao primeiro trabalho da disciplina

Despacho Termoeletrico de Usinas com ZOP - Aplicacao de ACO

Prof.: Ivo Chaves da Silva Júnior

"""

########################################################################################################################
### ... ::: BIBLIOTECAS UTILIZADAS ::: ... ###
import numpy as np
import os
import random

from cvxopt import matrix, solvers

from pt2_ACO_SEQ import ArmazenaDadosUsina

solvers.options['show_progress'] = False
# solvers.options['refinement'] = 2
solvers.options['maxiters'] = 15

### ... ::: FIM BIBLIOTECAS UTILIZADAS ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: FUNCAO CUSTO GERACAO ::: ... ###
'''
Essa funcao avalia o custo de despacho das usinas termoeletricas do problema proposto.
Ela ira retornar o FMINCON para a sequencia escolhida por cada formiga.
Para tanto, eh utilizada a biblioteca CVXOPT para solucao desse problema.

Para mais informacoes sobre a biblioteca CVXOPT, acesse:
https://courses.csail.mit.edu/6.867/wiki/images/a/a7/Qp-cvxopt.pdf
https://buildmedia.readthedocs.org/media/pdf/cvxopt/latest/cvxopt.pdf
'''

def CustoGeracao(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas, PD):
    # Dados das usinas selecionadas: caso de multiplas ZOPs
    Ants_dados = ArmazenaDadosUsina(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas)

    # Variaveis para armazenamento dos resultados obtidos pela otimizacao
    Pg_usinas = np.zeros((nAnts, total_ger))
    fval_usina = np.zeros((nAnts, total_ger))
    fval_total = np.zeros(nAnts)
    exitflag_ = []

    for i in range(0, nAnts):

        # Coeficientes: a, b & c - Equacionamento da FOB
        a = np.sum(Ants_dados[i, :, 1])
        b = Ants_dados[i, :, 2]
        c = Ants_dados[i, :, 3]

        # Coeficientes do CVXOPT - variaveis auxiliares
        aux_h = np.zeros(2 * c.shape[0])
        aux_A = np.ones(c.shape[0])
        aux_G1 = (-1) * np.eye(c.shape[0])
        aux_G2 = np.eye(c.shape[0])
        aux_G = np.concatenate((aux_G1, aux_G2))
        aux_P = np.zeros((c.shape[0], c.shape[0]))
        for ii in range(0, c.shape[0]):
            aux_P[ii, ii] = c[ii]
            aux_h[ii] = (-1) * Ants_dados[i, ii, 4]
            aux_h[ii + c.shape[0]] = Ants_dados[i, ii, 5]

        P = 2 * matrix(aux_P)  # armazena coeficientes quadraticos
        q = matrix(b)  # armazena coeficientes lineares

        G = matrix(aux_G)  # Matriz de Inequacoes
        h = matrix(aux_h)  # Limites das Inequacoes

        A = matrix(aux_A, (1, c.shape[0]))  # Matriz de Equacoes
        b = matrix(PD)  # Resultados das Equacoes

        # CVXOPT Quadratic Programming
        sol = solvers.qp(P, q, G, h, A, b)

        # Armazenamento de variaveis
        fval_total[i] = sol['dual objective'] + a  # Custo de Despacho Total
        exitflag_.append(sol['status'])  # Status CVXOPT QP

        # Penalizacao de solucoes nao otimas: Estrategia Big-Number
        if (sol['status'] != 'optimal'):
            fval_total[i] = 10 ** 10

        # Geracao por usina & Custo de Despacho por Usina
        for j in range(0, total_ger):

            Pg_usinas[i, j] = sol['x'][j]

            fval_usina[i, j] = Ants_dados[i, j, 3] * (Pg_usinas[i, j] ** 2) + \
                               Ants_dados[i, j, 2] * Pg_usinas[i, j] + \
                               Ants_dados[i, j, 1]

    # Retorna valores armazenados
    return Pg_usinas, fval_total, fval_usina, exitflag_


### ... ::: FIM FUNCAO CUSTO GERACAO ::: ... ###
########################################################################################################################

