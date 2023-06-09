%%                        Base de DADOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ==================== Sistema com 40 UTEs ================================
% ================= Zona de Operação Proibida =============================
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Demanda do sistema (PD)
PD = 7000;%MW

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                    Matriz de coeficientes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   UTE       a          b           c         Pmin  Pmax
%    1        2          3           4           5    6
Dados_Usinas = [
      1    170.44      8.336      0.03073       40   80;
      
      2    309.54      7.0706     0.2028        60   80; 
      2    309.54      7.0706     0.2028        85  120;
      
      3    369.03      8.1817     0.00942       80   82;
      3    369.03      8.1817     0.00942       88  190; 
      
      4    135.48      6.9467     0.08482       24   42;
      
      5    135.19      6.5595     0.09693       26   42;
      
      6    222.33      8.0543     0.01142       68  140;
      
      7    287.71      8.0323     0.0357       110  155;
      7    287.71      8.0323     0.0357       162  221;
      7    287.71      8.0323     0.0357       235  300;
      
      8    391.98      6.999      0.00492      135  300;
      
      9    455.76      6.602      0.00573      135  235;
      9    455.76      6.602      0.00573      246  300;
     
     10   722.82      12.908     0.00605      130  200;
     10   722.82      12.908     0.00605      211  300;
     
     11   635.2       12.986     0.00515       94  213;
     11   635.2       12.986     0.00515      220  375;
     
     12   654.69      12.796     0.00569       94  213;
     12   654.69      12.796     0.00569      220  375;
     
     13   913.4       12.501     0.00421      125  201;
     13   913.4       12.501     0.00421      211  290;
     13   913.4       12.501     0.00421      310  413;
     13   913.4       12.501     0.00421      425  500;
     
     14   1760.4      8.8412     0.00752      125  205;
     14   1760.4      8.8412     0.00752      217  306;
     14   1760.4      8.8412     0.00752      318  409;
     14   1760.4      8.8412     0.00752      420  500;
     
     15   1728.3      9.1575     0.00708      125  214;
     15   1728.3      9.1575     0.00708      230  277;
     15   1728.3      9.1575     0.00708      290  402;
     15   1728.3      9.1575     0.00708      412  500;
     
     16   1728.3      9.1575     0.00708      125  214;
     16   1728.3      9.1575     0.00708      230  277;
     16   1728.3      9.1575     0.00708      290  402;
     16   1728.3      9.1575     0.00708      412  500;
     
     17   1728.3      9.1575     0.00708      125  214;
     17   1728.3      9.1575     0.00708      230  277;
     17   1728.3      9.1575     0.00708      290  402;
     17   1728.3      9.1575     0.00708      412  500;
     
     18   647.85      7.9691     0.00313      220  307;
     18   647.85      7.9691     0.00313      321  407;
     18   647.85      7.9691     0.00313      421  500;
     
     19   649.69      7.955      0.00313      220  301;
     19   649.69      7.955      0.00313      310  421;
     19   649.69      7.955      0.00313      431  500;
     
     20   647.83      7.9691     0.00313      242  340;
     20   647.83      7.9691     0.00313      351  421;
     20   647.83      7.9691     0.00313      431  500;
     
     21   647.81      7.9691     0.00313      242  340;
     21   647.81      7.9691     0.00313      351  421;
     21   647.81      7.9691     0.00313      431  500;
     
     22   785.96      6.6313     0.00298      254   306;
     22   785.96      6.6313     0.00298      320   440;
     22   785.96      6.6313     0.00298      445   550;
     
     23   785.96      6.6313     0.00298      254   306;
     23   785.96      6.6313     0.00298      320   440;
     23   785.96      6.6313     0.00298      445   550;          
     
     24   794.53      6.6611     0.00284      254   370;
     24   794.53      6.6611     0.00284      390   495;
     24   794.53      6.6611     0.00284      502   550;
     
     25   794.53      6.6611     0.00284      254   370;
     25   794.53      6.6611     0.00284      390   495;
     25   794.53      6.6611     0.00284      502   550;
     
     
     26   801.32      7.1032     0.00277      254   380;
     26   801.32      7.1032     0.00277      410   501;
     26   801.32      7.1032     0.00277      520   550;
     
     27   801.32      7.1032     0.00277      254   380;
     27   801.32      7.1032     0.00277      410   501;
     27   801.32      7.1032     0.00277      520   550;
     
     28   1055.1      3.3353     0.52124       10   102;
     28   1055.1      3.3353     0.52124      113   150;
     
     29   1055.1      3.3353     0.52124       10   102;
     29   1055.1      3.3353     0.52124      113   150;
     
     30   1055.1      3.3353     0.52124       10   102;
     30   1055.1      3.3353     0.52124      113   150;
     
     31   1207.8      13.052     0.25098       20    70;
     
     32   810.79      21.887     0.16766       20    70;
     
     33   1247.7      10.244     0.2635        20    70;
     
     34   1219.2      8.3707     0.30575       20    70;
     
     35   641.43      26.258     0.18362       18    60;
     
     36   1112.8      9.6956     0.32563       18    60;
     
     37   1044.4      7.1633     0.33722       20    60;
     
     38   832.24      16.339     0.23915       25    60;
     
     39   834.24      16.339     0.23915       25    60;

     40   1035.2      16.339     0.23915       25    60;
];