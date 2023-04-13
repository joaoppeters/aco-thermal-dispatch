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

Despacho Termoeletrico de Usinas com ZOP - Aplicacao de ACO

Prof.: Ivo Chaves da Silva Júnior

"""

########################################################################################################################
### ... ::: BIBLIOTECAS UTILIZADAS ::: ... ###
import imageio
import matplotlib.pyplot as plt
import numpy as np

### ... ::: FIM BIBLIOTECAS UTILIZADAS ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: FUNCAO PNG PLOT ::: ... ###
def PNGIFPLOT(file, iter, iter_max, nzop_ger, total_ger, MFero, Images, nAnts):

    fig, ax = plt.subplots(1, figsize=(9, 6))
    bar_width = 0.15
    colors = ['r', 'b', 'g', 'y']
    for ute in range(0, int(np.max(nzop_ger))):
        plt.gca()
        if file == 'Sistema_10_ZP':
            plt.bar(np.arange(1, total_ger + 1) + (ute * bar_width) - bar_width, MFero[:, ute], bar_width, alpha=0.4, color=colors[ute])
        else:
            plt.bar(np.arange(1, total_ger + 1) + (ute * bar_width) - (3/2) * bar_width, MFero[:, ute], bar_width, alpha=0.4, color=colors[ute])
    plt.title('Gráfico do Comportamento Dinâmico do Feromônio \n{} Formigas -- {} Iterações'.format(nAnts, iter+1))
    plt.xlabel('Usinas & ZOPs')
    plt.ylabel('Rastro de Feromônio')
    plt.xticks(np.arange(1, total_ger + 1))
    if file == 'Sistema_40_ZP':
        plt.xticks(rotation=90)
    plt.legend(['UTE ZOP 1', 'UTE ZOP 2', 'UTE ZOP 3', 'UTE ZOP 4'], framealpha=0.9, edgecolor='white')
    plt.pause(0.001)
    if (iter < iter_max - 1):
        plt.close()

    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    Images.append(image)

    return plt, Images
### ... ::: FIM FUNCAO PNG PLOT ::: ... ###
########################################################################################################################


########################################################################################################################
### ... ::: FUNCAO BEST SEQ PLOT ::: ... ###

def BESTPLOT(best_fit, iteris, cte_N, cte_S):

    fig, ax = plt.subplots(2, figsize=(9, 6))
    plt.title('Trajetórias de Convergência')
    plt.xlabel('Iterações')
    plt.ylabel('Valor Fitness')

    colors = ['r', 'b', 'g', 'y']

    c = 0
    for n in cte_n:
        for s in cte_s:
            c += 1
            plt.plot(iteris['{}'.format(n)]['{}'.format(s)], best_fit['{}'.format(n)]['{}'.format(s)], legend='C{}'.format(c), color=colors[n])

    plt.legend()

    plt.savefig(pwd + '/CasosTrajetoriaConvergencia.png', format='png')



### ... ::: FIM FUNCAO BEST SEQ PLOT ::: ... ###
########################################################################################################################
