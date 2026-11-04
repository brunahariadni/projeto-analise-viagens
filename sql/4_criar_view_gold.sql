USE transparencia;

CREATE OR REPLACE VIEW vw_gold_resumo_orgao AS

WITH pagamentos AS (
    SELECT
        id_viagem,
        SUM(valor) AS total_pagamentos
    FROM silver_pagamento
    GROUP BY id_viagem
),

passagens AS (
    SELECT
        id_viagem,
        COUNT(*) AS quantidade_passagens
    FROM silver_passagem
    GROUP BY id_viagem
),

trechos AS (
    SELECT
        id_viagem,
        COUNT(*) AS quantidade_trechos
    FROM silver_trecho
    GROUP BY id_viagem
)

SELECT
    v.nome_orgao_superior,
    COUNT(DISTINCT v.id_viagem) AS quantidade_viagens,
    ROUND(SUM(v.valor_total), 2) AS custo_total,
    ROUND(AVG(v.valor_total), 2) AS custo_medio,
    ROUND(SUM(COALESCE(p.total_pagamentos, 0)), 2) AS total_pagamentos,
    SUM(COALESCE(pa.quantidade_passagens, 0)) AS quantidade_passagens,
    SUM(COALESCE(t.quantidade_trechos, 0)) AS quantidade_trechos

FROM silver_viagem v

LEFT JOIN pagamentos p
    ON v.id_viagem = p.id_viagem

LEFT JOIN passagens pa
    ON v.id_viagem = pa.id_viagem

LEFT JOIN trechos t
    ON v.id_viagem = t.id_viagem

GROUP BY
    v.nome_orgao_superior;