# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

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

Despacho Economico de Usinas Termoeletricas com ZOP - Aplicacao de ACO

Prof.: Ivo Chaves da Silva Júnior

"""

# ------------------------------------------------------------------------------------------------- #
# ------------------------------------ BIBLIOTECAS UTILIZADAS ----------------------------------- #
import imageio
import numpy as np
import os
import random
import timeit

from oct2py import octave as oct
from scipy.io import loadmat

from pt1_ACO_CVXOPT import CustoGeracao
from pt3_ACO_PLOT import PNGIFPLOT, BESTPLOT

### ... ::: FIM BIBLIOTECAS UTILIZADAS ::: ... ###
########################################################################################################################

pwd = os.getcwd()
start = timeit.default_timer()

########################################################################################################################
### ... ::: LEITURA DE ARQUIVOS ::: ... ###
# Base de Dados Utilizadas: escolher uma, comentar as outras.
# Cada base de dados retorna as caracte_Nristicas das usinas, suas zop e a
# demanda eletrica total do problema.
# file = 'Sistema_10_ZP'
# file = 'Sistema_15_ZP'
file = 'Sistema_40_ZP'

# Leitura do Arquivo
path_file = pwd + '/' + file + '.mat'
if os.path.isfile(path_file) is False:
    oct.eval('cd ' + pwd)
    oct.eval(file)
    oct.eval('save -v7 ' + file + '.mat')

# Armazenamento dos valores lidos em variaveis
D = loadmat(path_file)
PD = D['PD'][0][0]
Dados_Usinas = D['Dados_Usinas']

### ... ::: FIM LEITURA DE ARQUIVOS ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: DADOS DA COLONIA & SOLUCOES INICIAIS ::: ... ###

# Numero de Geradores
nger = Dados_Usinas[:, 0]
total_ger = int(np.amax(nger))

# Numero de ZOPs por gerador
nzop_ger = np.zeros(total_ger, dtype='int8')
aux = 0

nzop_ger[aux] = 1
for i in range(1, nger.shape[0]):

    if nger[i] != nger[i - 1]:

        aux = aux + 1

    nzop_ger[aux] += 1


# Numero de Formigas na Colonia
nAnts = 100

# Escolha inicial das formigas
Ants = np.zeros((nAnts, total_ger), dtype='int8')

for frmg in range(0, nAnts):

    for usina in range(0, total_ger):

        if (nzop_ger[usina] > 1):

            Ants[frmg, usina] = 1 + np.round(random.random()  * (nzop_ger[usina] - 1))

        else:

            Ants[frmg, usina] = 1

### ... ::: FIM DADOS DA COLONIA & SOLUCOES INICIAIS ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: PROCESSO ITERATIVO - COLONIA DE FORMIGAS ::: ... ###
# Parametro da Evaporacao
sigma_best = 0.05
sigma = 0.25
sigma_worst = 0.75

# Dimensao da Matriz de Feromonio
MFero = np.zeros((total_ger, int(np.max(nzop_ger))))

# Numero maximo de iteracoes
maxIter = 200

# Variavel para armazenar melhor valor da FOB
best_fval = np.inf
worst_fval = -np.inf

# Para Montagem de GIFs
Images = []

# Processo Iterativo
for iter in range(maxIter):

    # CVXOPT de cada Formiga
    Pg_usinas, fval_total, fval_usina, exitflag_ = CustoGeracao(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas, PD)

    # Menor valor obtido entre as escolhas das formigas
    fval_min = np.min(fval_total)
    idx_min = np.argmin(fval_total)

    # Maior valor obtido entre as escolhas das formigas
    fval_max = np.max(fval_total)
    idx_max = np.argmax(fval_total)

    # Armazenamento do valor otimo
    if (fval_min < best_fval):

        best_idx = idx_min

        best_fval = fval_min

        best_seq = Ants[idx_min, :].copy()

        best_ger = Pg_usinas[idx_min, :].copy()

        best_iter = iter + 1

    # Armazenamento do pior valor
    if (fval_max > worst_fval):

        worst_idx = idx_max

        worst_fval = fval_max

        worst_seq = Ants[idx_max, :].copy()

        worst_ger = Pg_usinas[idx_max, :].copy()

        worst_iter = iter + 1

    #--------------------------------------------------------------#
    # CONSTRUCAO DAS SOLUCOES - ATUALIZACAO DA MATRIZ DE FEROMONIO #
    #--------------------------------------------------------------#
    for frmg in range(0, nAnts):

        for ute in range(0, total_ger):

            zop_ute = Ants[frmg, ute] - 1

            MFero[ute, zop_ute] = MFero[ute, zop_ute] + (1 / fval_total[frmg])


    #-------------------------------------------------------------------------------------------#
    # MONTAGEM DA ROLETA (DETERMINACAO DO PERCENTUAL DE CADA SOLUCAO ENCONTRADA PELAS FORMIGAS) #
    #-------------------------------------------------------------------------------------------#
    for usina in range(0, total_ger):

        # Apenas para usinas com ZOPs > 1
        if (nzop_ger[usina] > 1):

            # Total de Feromonio da Usina
            Total_MFero = np.sum(MFero[usina, :])

            # Pedaco da Roleta referente a solucao
            pct = np.round((MFero[usina, :] / Total_MFero) * 100)

            # Posicoes com rastro de Feromonio
            rastro = np.where(pct > 0)[0]

            # Determinacao do numero de elementos/posicoes com rastros de feromonio
            ncol = rastro.shape[0]

            # Contagem do numero de fatias de cada solucao
            cont = 0

            # Guarda ponto de troca das fatias/solucoes dentro da roleta
            guarda = 0

            cassino_col = []
            for j in range(0, ncol):

                while (cont < pct[rastro[j]] + guarda - 1):

                    cont += 1
                    cassino_col.append(j)

                guarda = cont

            COL = len(cassino_col)

            #-------------------------------------------------#
            # SORTEIO DAS SOLUCOES COM BASE NA ROLETA MONTADA #
            #-------------------------------------------------#
            for ant in range(0, nAnts):

                decisao = random.random() * 100

                # Formigas SEGUEM o rastro de Feromonio (80% de chance)
                if decisao <= 80:

                    # Roleta em movimento
                    sorteio = np.round(random.random() * (COL - 1)) + 1

                    # Roleta parada
                    posicao = cassino_col[int(sorteio - 1)]

                    # Valor da raiz
                    Ants[ant, usina] = rastro[posicao] + 1

                # Formigas procuram outra solucao ALEATORIA (20% de chance)
                else:

                    # Valor da raiz
                    Ants[ant, usina] = random.randint(1, nzop_ger[usina])

    #-----------------------------------#
    # EVAPORACAO DA MATRIZ DE FEROMONIO #
    #-----------------------------------#
    # Atualizacao dinamica
    for row in range(0, total_ger):

        if (nzop_ger[row] == 1):

            MFero[row, 0] = (1 - sigma_best) * MFero[row, 0]

        else:

            for col in range(0, nzop_ger[row]):

                if (col + 1 == best_seq[row]):

                    MFero[row, col] = (1 - sigma_best) * MFero[row, col]

                elif (col + 1 == worst_seq[row]):

                    MFero[row, col] = (1 - sigma_worst) * MFero[row, col]

                else:

                    MFero[row, col] = (1 - sigma) * MFero[row, col]


    #---------------------------------------------------------#
    # GRAFICO DO COMPORTAMENTO: ANALISE DINAMICA DO FEROMONIO #
    #---------------------------------------------------------#
    plt, Images = PNGIFPLOT(file, iter, maxIter, nzop_ger, total_ger, MFero, Images, nAnts)

imageio.mimsave(pwd + '/CVXOPT_{}_{}Formigas_{}iter.gif'.format(file, nAnts, maxIter), Images, fps=10)
plt.savefig(pwd + '/CVXOPT_{}_{}Formigas_{}iter.png'.format(file, nAnts, maxIter), format='png')


### ... ::: FIM DO PROCESSO ITERATIVO - COLONIA DE FORMIGAS ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: ORGANIZACAO FINAL ::: ... ###

stop = timeit.default_timer()

print(stop - start)

print(best_fval, worst_fval)

print(best_seq, worst_seq)

print(best_ger, worst_ger)

print(best_iter, worst_idx)

print(best_idx, worst_idx)

### ... ::: FIM ORGANIZACAO FINAL ::: ... ###
########################################################################################################################
