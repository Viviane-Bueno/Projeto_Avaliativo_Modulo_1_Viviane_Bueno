-- 0_criar_banco.sql - VERSÃO POSTGRESQL
DROP TABLE IF EXISTS silver_trecho CASCADE;
DROP TABLE IF EXISTS silver_passagem CASCADE;
DROP TABLE IF EXISTS silver_pagamento CASCADE;
DROP TABLE IF EXISTS silver_viagem CASCADE;

DROP TABLE IF EXISTS raw_trecho;
DROP TABLE IF EXISTS raw_passagem;
DROP TABLE IF EXISTS raw_pagamento;
DROP TABLE IF EXISTS raw_viagem;

-- ==================== CAMADA RAW (tudo VARCHAR, sem constraints) ====================

CREATE TABLE raw_viagem (
    id_viagem VARCHAR(20),
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(10),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(500),
    cpf_viajante VARCHAR(20),
    nome_viajante VARCHAR(500),
    cargo VARCHAR(500),
    funcao VARCHAR(500),
    data_inicio VARCHAR(20),
    data_fim VARCHAR(20),
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias VARCHAR(50),
    valor_passagens VARCHAR(50),
    valor_devolucao VARCHAR(50),
    valor_outros_gastos VARCHAR(50)
);

CREATE TABLE raw_pagamento (
    id_viagem VARCHAR(20),
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(500),
    nome_ug_pagadora VARCHAR(500),
    tipo_pagamento VARCHAR(100),
    valor VARCHAR(50)
);

CREATE TABLE raw_passagem (
    id_viagem VARCHAR(20),
    meio_transporte VARCHAR(100),
    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(100),
    cidade_origem_ida VARCHAR(100),
    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(100),
    cidade_destino_ida VARCHAR(100),
    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(100),
    cidade_origem_volta VARCHAR(100),
    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(100),
    cidade_destino_volta VARCHAR(100),
    valor_passagem VARCHAR(50),
    taxa_servico VARCHAR(50),
    data_emissao VARCHAR(20)
);

CREATE TABLE raw_trecho (
    id_viagem VARCHAR(20),
    sequencia_trecho VARCHAR(20),
    origem_data VARCHAR(20),
    origem_uf VARCHAR(100),
    origem_cidade VARCHAR(100),
    destino_data VARCHAR(20),
    destino_uf VARCHAR(100),
    destino_cidade VARCHAR(100),
    meio_transporte VARCHAR(100),
    numero_diarias VARCHAR(50)
);

-- ==================== CAMADA SILVER (tipada + PK + FK + Constraints) ====================

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
    CONSTRAINT chk_viagem_diarias CHECK (valor_diarias >= 0)
);

CREATE TABLE silver_pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2),
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_pag_valor CHECK (valor >= 0)
);

CREATE TABLE silver_passagem (
    id_passagem SERIAL PRIMARY KEY,
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
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_pass_valor CHECK (valor_passagem >= 0),
    CONSTRAINT chk_pass_taxa CHECK (taxa_servico >= 0)
);

CREATE TABLE silver_trecho (
    id_trecho SERIAL PRIMARY KEY,
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
    FOREIGN KEY (id_viagem) REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_trecho_diarias CHECK (numero_diarias >= 0),
    CONSTRAINT uq_viagem_sequencia UNIQUE (id_viagem, sequencia_trecho)
);