% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [210115] - Topicos Especiais em Otimizacao: Tecnicas Inteligentes       %
%                                                                         %
% TRABALHO: DESPACHO TERMOELETRICO COM ZOP - APLICACAO AOA                %
%                                                                         %
% Joao Pedro Peters Barbosa & Pedro Henrique Peters Barbosa               %
% (ls)                                                                    %
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

function [Pg_usinas, fval_total, fval_usina, exitflag_] = pt1_Formiga_CustoGeracao(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas, PD)

% Dados das usinas selecionadas: caso de multiplas zop
Ants_dados = pt2_Formiga_ArmazenaDadosUsina(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas);

Pg_usinas = zeros(nAnts, total_ger);
fval_usina = zeros(nAnts, total_ger);
fval_total = zeros(1, nAnts);
exitflag_ = zeros(1, nAnts);

for i=1:nAnts
   
    % Coeficientes para equacionamento
    a = sum(Ants_dados(i, :, 2));
    b = Ants_dados(i, :, 3);
    c = Ants_dados(i, :, 4);
   
    % Limites Inferior e Superior
    lb = Ants_dados(i, :, 5)';
    ub = Ants_dados(i, :, 6)';
   
    % Matriz de Igualdade
    Aeq = ones(1, total_ger);
    Beq = PD;
    
    % Chute Inicial
    x0 = lb;
   
    % Equacionamento da FOB
    fob = @(x) (a + sum(x.*b' + (x.^2).*c'));
    
    % Formulacao do FMINCON
    opt = optimset('Display', 'off');
    [Pg, fval, exitflag] = fmincon(fob, x0, [], [], Aeq, Beq, lb, ub, [], opt);
   
    % Estrategia Big-Number - Penalizacao de solucoes nao otimas
    if exitflag ~= 1
    
        fval = 10^10;
    
    end
    
    % Armazenamento de variaveis
    Pg_usinas(i, :) = Pg;
    fval_total(i) = fval;
    exitflag_(i) = exitflag;
    
    % Custo de geracao por usina
    for j=1:total_ger
       
       fval_usina(i, j) = Ants_dados(i, j, 2) + ...
           Ants_dados(i, j, 3)*Pg_usinas(i, j) + ...
           Ants_dados(i, j, 4)*Pg_usinas(i, j)^2;
        
    end
    
end
