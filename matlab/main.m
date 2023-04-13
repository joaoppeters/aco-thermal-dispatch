% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [210115] - Topicos Especiais em Otimizacao: Tecnicas Inteligentes       %
%                                                                         %
% TRABALHO: DESPACHO TERMOELETRICO COM ZOP - APLICACAO ACO                %
% Prof. Ivo Chaves da Silva Júnior                                        %
%                                                                         %
% Joao Pedro Peters Barbosa & Pedro Henrique Peters Barbosa               %
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

clear all; close all; clc; warning off;

%% Leitura do arquivo

% Base de Dados Utilizadas: escolher uma, comentar as outras. 
% Cada base de dados retorna as caracteristicas das usinas, suas zop e a 
% demanda eletrica total do problema.
% Sistema_10_ZP;
Sistema_15_ZP;
% Sistema_40_ZP;

%% Determinacao das variaveis
% Numero de Geradores
nger = Dados_Usinas(:, 1);
total_ger = max(nger);

% Detalhamento da ZOP de cada usina: unica ou multipla ZOP
nzop_ger = 1;
aux = 1;

for i=2:length(nger)
    
    if nger(i) ~= nger(i-1)
        
        aux = aux + 1;
        
        nzop_ger(aux) = 0;
        
    end
    
   nzop_ger(aux) = nzop_ger(aux) + 1;
    
end


%% Inicializacao da colonia de formigas & solucao de entrada
% Numero de Formigas na Colonia
nAnts = 100;

% Escolha Inicial das Formigas
Ants = zeros(nAnts, total_ger);

for frmg=1:nAnts
    
    for usina=1:total_ger
        
        if nzop_ger(usina) > 1
            
            Ants(frmg, usina) = 1 + round((rand * (nzop_ger(usina) - 1)));
            
        else
            
            Ants(frmg, usina) = 1;
            
        end
    end
end


%% Otimizacao por Colonia de Formigas
% Parametros da evaporacao
sigma_best = 0.05;
sigma = 0.25;
sigma_worst = 0.75;

% Dimensao matriz feromonio
MFero = zeros(total_ger, max(nzop_ger));

% Numero maximo de iteracoes
maxIter = 200;

% Variaveis para armazenar melhor e pior valor da FOB
best_fval = inf;
worst_fval = -inf

tic
% Processo Iterativo
for iter=1:maxIter
    
    clc;
    iter
    
    % FMINCON de cada Formiga
    [Pg_usinas, fval_total, fval_usina, exitflag_] = pt1_Formiga_CustoGeracao(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas, PD);
    
    % Armazenamento do melhor valor fitness 
    [fval_min, idx_min] = min(fval_total);
    
    if fval_min < best_fval
        
        best_idx = idx_min;
        
        best_fval = fval_min;
        
        best_seq = Ants(idx_min, :);
        
        best_ger = Pg_usinas(idx_min, :);
        
        best_iter = iter;
        
    end
    
    
    % Armazenamento do pior valor fitness
    [fval_max, idx_max] = max(fval_total);
    
    if fval_max > worst_fval
        
        worst_idx = idx_max;
        
        worst_fval = fval_max;
        
        worst_seq = Ants(idx_max, :);
        
        worst_ger = Pg_usinas(idx_max, :);
        
        worst_iter = iter;
        
    end
   
    %#############################################################
    % CONSTRUCAO DAS SOLUCOES - ATUALIZACAO DA MATRIZ DE FEROMONIO
    %#############################################################
    for frmg=1:nAnts
        
        for ute=1:total_ger

            zop_ute = Ants(frmg, ute);

            MFero(ute, zop_ute) = MFero(ute, zop_ute) + (1 / fval_total(frmg));

        end
        
    end
    
    %######################################################################################### 
    % MONTAGEM DA ROLETA (DETERMINACAO DO PERCENTUAL DE CADA SOLUCAO ENCONTRADA PELAS FORMIGAS
    %#########################################################################################
    for usina=1:total_ger

        if nzop_ger(usina) > 1

            % TOTAL FEROMONIO USINA
            Total_MFero = sum(MFero(usina, :));

            % PEDACO DA ROLETA REFERENTE A SOLUCAO
            pct = round((MFero(usina, :) / Total_MFero) * 100);

            % POSICOES COM RASTRO DE FEROMONIO
            rastro = find(pct > 0);

            % DETERMINACAO DO NUMERO DE ELEMENTOS/POSICOES COM RASTROS DE FEROMONIO 
            ncol = size(rastro, 2);

            % CONTAGEM DO NUMERO DE FATIAS DE CADA SOLUCAO
            cont = 0;

            % GUARDA O PONTO DE TROCA DAS FATIAS (SOLUCOES) DENTRO DA ROLETA  
            guarda = 0;
            cassino_col = [];

            for j=1:ncol

                while cont < pct(rastro(j)) + guarda

                     cont = cont + 1;
                     cassino_col(cont) = j;

                end

                guarda = cont;

            end


            COL = size(cassino_col, 2);


            %################################################
            % SORTEIO DAS SOLUCOES COM BASE NA ROLETA MONTADA
            %################################################
            for ant=1:nAnts
                
                DECISAO = rand*100;

                % FORMIGAS SEGUEM O RASTRO DE FEROMONIO
                if DECISAO <= 80

                   % RODO A ROLETA
                   sorteio = round(rand(1) * (COL - 1)) + 1;

                    % POSICAO OBTIDA PELO CASSINO
                   posicao = cassino_col(sorteio);

                   % VALOR DA RAIZ
                    Ants(ant, usina) = rastro(posicao);

               % FORMIGAS SEGUEM CAMINHO ALEATORIO
               else

                   % VALOR DA RAIZ
                   Ants(ant, usina) = randi([1, nzop_ger(usina)]);

                end
               
            end

        end

   end
       
             
    %###################################
    %  EVAPORACAO DA MATRIZ DE FEROMONIO
    %###################################
    % Atualizacao dinamica
    for row = 1:total_ger
        
        if (nzop_ger(row) == 1)
            
            MFero(row, 1) = (1 - sigma_best) * MFero(row, 1);
        
        else
            
            for col = 1:nzop_ger(row)
                
                if (col == best_seq(row))
                    
                    MFero(row, col) = (1 - sigma_best) * MFero(row, col);
                
                elseif (col == worst_seq(row))
                    
                    MFero(row, col) = (1 - sigma_worst) * MFero(row, col);
                
                else 
                    
                    MFero(row, col) = (1 - sigma) * MFero(row, col);
                end
            end
        end
    end
    

    
    bar(MFero);
    figure(gcf);
    title('GRAFICO DO COMPORTAMENTO DINAMICO DO FEROMONIO');
    xlabel('Usinas & ZOPs');
    ylabel('RASTRO DE FEROMONIO');
    pause(0.3);
   
end

toc

format long g
best_fval

format short g
best_seq
best_ger
