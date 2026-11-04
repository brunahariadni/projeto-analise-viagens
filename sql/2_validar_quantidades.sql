USE transparencia;

SELECT 'silver_viagem' AS tabela, COUNT(*) AS registros
FROM silver_viagem

UNION ALL

SELECT 'silver_pagamento', COUNT(*)
FROM silver_pagamento

UNION ALL

SELECT 'silver_passagem', COUNT(*)
FROM silver_passagem

UNION ALL

SELECT 'silver_trecho', COUNT(*)
FROM silver_trecho;