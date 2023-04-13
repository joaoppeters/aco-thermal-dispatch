


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

### ... ::: FIM BIBLIOTECAS UTILIZADAS ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: FUNCAO ARMAZENAMENTO DE DADOS DAS USINAS ::: ... ###
'''
Essa funcao armazena os dados de cada usina respeitando a zona operativa selecionada pela formiga.
A funcao acessa os dados lidos nos arquivos '.m' (armazenado na variavel Dados_Usinas)
e retorna uma variavel (Ants_dados) que armazena os valores de: a; b; c; Pmn; Pmax, respectivos da UTE/ZOP escolhida.
'''

def ArmazenaDadosUsina(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas):
    # Dados das Usinas selecionadas: caso de multiplas ZOPs
    Ants_dados = np.zeros((nAnts, total_ger, Dados_Usinas.shape[1]))

    for frmg in range(0, nAnts):
        # Variavel auxiliar para selecionar dados corretos da usina
        row = 0

        for usina in range(0, total_ger):

            if (nzop_ger[usina] > 1):

                row = row + Ants[frmg, usina] - 1

            for dados in range(0, Dados_Usinas.shape[1]):

                Ants_dados[frmg, usina, dados] = Dados_Usinas[row, dados]

            row = row + nzop_ger[usina] - Ants[frmg, usina] + 1


    # Retorna variavel que armazenou todas os dados da usina-zop
    return Ants_dados

### ... ::: FUNCAO ARMAZENAMENTO DE DADOS DAS USINAS ::: ... ###
########################################################################################################################
