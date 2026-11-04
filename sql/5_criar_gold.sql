USE transparencia;

CREATE TABLE IF NOT EXISTS gold_resumo_orgao (
    nome_orgao_superior VARCHAR(255) PRIMARY KEY,
    quantidade_viagens BIGINT NOT NULL DEFAULT 0,
    custo_total DECIMAL(34,2),
    custo_medio DECIMAL(13,2),
    total_pagamentos DECIMAL(54,2),
    quantidade_passagens DECIMAL(42,0),
    quantidade_trechos DECIMAL(42,0)
);

-- Atualiza os dados da tabela Gold
DELETE FROM gold_resumo_orgao;

INSERT INTO gold_resumo_orgao (
    nome_orgao_superior,
    quantidade_viagens,
    custo_total,
    custo_medio,
    total_pagamentos,
    quantidade_passagens,
    quantidade_trechos
)
SELECT
    nome_orgao_superior,
    quantidade_viagens,
    custo_total,
    custo_medio,
    total_pagamentos,
    quantidade_passagens,
    quantidade_trechos
FROM vw_gold_resumo_orgao;