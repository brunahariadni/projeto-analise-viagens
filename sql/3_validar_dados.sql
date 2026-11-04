SELECT
    (SELECT COUNT(*)
     FROM silver_viagem
     WHERE data_fim < data_inicio) AS datas_invertidas,

    (SELECT COUNT(*)
     FROM silver_viagem
     WHERE duracao_dias < 0) AS duracoes_negativas,

    (SELECT COUNT(*)
     FROM silver_viagem
     WHERE valor_diarias < 0
        OR valor_passagens < 0
        OR valor_devolucao < 0
        OR valor_outros_gastos < 0) AS valores_negativos,

    (SELECT COUNT(*)
     FROM silver_viagem
     WHERE nome_orgao_superior IS NULL) AS orgaos_vazios;