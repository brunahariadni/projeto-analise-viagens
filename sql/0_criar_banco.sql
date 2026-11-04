
CREATE DATABASE IF NOT EXISTS transparencia;
USE transparencia;

-- =====================================================
-- 1. REMOÇÃO DAS TABELAS EXISTENTES
-- Executar somente para recriar a estrutura do zero.
-- ATENÇÃO: os dados existentes serão apagados.
-- =====================================================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS silver_trecho;
DROP TABLE IF EXISTS silver_passagem;
DROP TABLE IF EXISTS silver_pagamento;
DROP TABLE IF EXISTS silver_viagem;

DROP TABLE IF EXISTS raw_trecho;
DROP TABLE IF EXISTS raw_passagem;
DROP TABLE IF EXISTS raw_pagamento;
DROP TABLE IF EXISTS raw_viagem;

SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- 2. CAMADA RAW
-- =====================================================

CREATE TABLE raw_viagem (
    `Identificador do processo de viagem` VARCHAR(255),
    `Número da Proposta (PCDP)` VARCHAR(255),
    `Situação` VARCHAR(255),
    `Viagem Urgente` VARCHAR(255),
    `Justificativa Urgência Viagem` VARCHAR(1000),
    `Código do órgão superior` VARCHAR(255),
    `Nome do órgão superior` VARCHAR(255),
    `Código órgão solicitante` VARCHAR(255),
    `Nome órgão solicitante` VARCHAR(255),
    `CPF viajante` VARCHAR(255),
    `Nome` VARCHAR(255),
    `Cargo` VARCHAR(255),
    `Função` VARCHAR(255),
    `Descrição Função` VARCHAR(255),
    `Período - Data de início` VARCHAR(255),
    `Período - Data de fim` VARCHAR(255),
    `Destinos` VARCHAR(1000),
    `Motivo` VARCHAR(1000),
    `Valor diárias` VARCHAR(255),
    `Valor passagens` VARCHAR(255),
    `Valor devolução` VARCHAR(255),
    `Valor outros gastos` VARCHAR(255)
);

CREATE TABLE raw_pagamento (
    `Identificador do processo de viagem` VARCHAR(255),
    `Número da Proposta (PCDP)` VARCHAR(255),
    `Código do órgão superior` VARCHAR(255),
    `Nome do órgão superior` VARCHAR(255),
    `Codigo do órgão pagador` VARCHAR(255),
    `Nome do órgao pagador` VARCHAR(255),
    `Código da unidade gestora pagadora` VARCHAR(255),
    `Nome da unidade gestora pagadora` VARCHAR(255),
    `Tipo de pagamento` VARCHAR(255),
    `Valor` VARCHAR(255)
);

CREATE TABLE raw_passagem (
    `Identificador do processo de viagem` VARCHAR(255),
    `Número da Proposta (PCDP)` VARCHAR(255),
    `Meio de transporte` VARCHAR(255),
    `País - Origem ida` VARCHAR(255),
    `UF - Origem ida` VARCHAR(255),
    `Cidade - Origem ida` VARCHAR(255),
    `País - Destino ida` VARCHAR(255),
    `UF - Destino ida` VARCHAR(255),
    `Cidade - Destino ida` VARCHAR(255),
    `País - Origem volta` VARCHAR(255),
    `UF - Origem volta` VARCHAR(255),
    `Cidade - Origem volta` VARCHAR(255),
    `Pais - Destino volta` VARCHAR(255),
    `UF - Destino volta` VARCHAR(255),
    `Cidade - Destino volta` VARCHAR(255),
    `Valor da passagem` VARCHAR(255),
    `Taxa de serviço` VARCHAR(255),
    `Data da emissão/compra` VARCHAR(255),
    `Hora da emissão/compra` VARCHAR(255)
);

CREATE TABLE raw_trecho (
    `Identificador do processo de viagem` VARCHAR(255),
    `Número da Proposta (PCDP)` VARCHAR(255),
    `Sequência Trecho` VARCHAR(255),
    `Origem - Data` VARCHAR(255),
    `Origem - País` VARCHAR(255),
    `Origem - UF` VARCHAR(255),
    `Origem - Cidade` VARCHAR(255),
    `Destino - Data` VARCHAR(255),
    `Destino - País` VARCHAR(255),
    `Destino - UF` VARCHAR(255),
    `Destino - Cidade` VARCHAR(255),
    `Meio de transporte` VARCHAR(255),
    `Número Diárias` VARCHAR(255),
    `Missao?` VARCHAR(255)
);

-- =====================================================
-- 3. CAMADA SILVER
-- =====================================================

CREATE TABLE silver_viagem (
    id_viagem VARCHAR(20) PRIMARY KEY,
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT,
    CONSTRAINT chk_viagem_diarias
        CHECK (valor_diarias >= 0)
);

CREATE TABLE silver_pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2),
    CONSTRAINT chk_pagamento_valor
        CHECK (valor >= 0),
    CONSTRAINT fk_pagamento_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem)
);

CREATE TABLE silver_passagem (
    id_passagem INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    meio_transporte VARCHAR(50),
    pais_origem_ida VARCHAR(60),
    uf_origem_ida VARCHAR(40),
    cidade_origem_ida VARCHAR(80),
    pais_destino_ida VARCHAR(60),
    uf_destino_ida VARCHAR(40),
    cidade_destino_ida VARCHAR(80),
    valor_passagem DECIMAL(10,2),
    taxa_servico DECIMAL(10,2),
    data_emissao DATE,
    CONSTRAINT chk_passagem_valor
        CHECK (valor_passagem >= 0),
    CONSTRAINT chk_passagem_taxa
        CHECK (taxa_servico >= 0),
    CONSTRAINT fk_passagem_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem)
);

CREATE TABLE silver_trecho (
    id_trecho INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    sequencia_trecho INT,
    origem_data DATE,
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data DATE,
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2),
    CONSTRAINT chk_trecho_diarias
        CHECK (numero_diarias >= 0),
    CONSTRAINT uq_trecho_viagem_sequencia
        UNIQUE (id_viagem, sequencia_trecho),
    CONSTRAINT fk_trecho_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem)
);

-- =====================================================
-- 4. CONFERÊNCIA DAS TABELAS
-- =====================================================

SHOW TABLES;