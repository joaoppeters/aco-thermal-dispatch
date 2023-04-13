% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% [210115] - Topicos Especiais em Otimizacao: Tecnicas Inteligentes       %
%                                                                         %
% TRABALHO: DESPACHO TERMOELETRICO COM ZOP - APLICACAO AOA                %
%                                                                         %
% Joao Pedro Peters Barbosa & Pedro Henrique Peters Barbosa               %
% (ls)                                                                    %
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

function [Ants_dados]=pt2_Formiga_ArmazenaDadosUsina(nAnts, Ants, total_ger, nzop_ger, Dados_Usinas)
    
% Dados das usinas selecionadas: caso de multiplas zop
Ants_dados = zeros(nAnts, total_ger, size(Dados_Usinas, 2));

for frmg=1:nAnts
    
    row = 1;
    
   for usina=1:total_ger
       
      if nzop_ger(usina) > 1
          
        row = row + Ants(frmg, usina) - 1;
        
      end
      
       for dados=1:size(Dados_Usinas, 2)
           
          Ants_dados(frmg, usina, dados) = Dados_Usinas(row, dados); 
          
       end
       
      row = row + nzop_ger(usina) - Ants(frmg, usina) + 1;
      
   end
   
end
