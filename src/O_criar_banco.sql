-- Criação do Banco de Dados (execute se necessário)
-- CREATE DATABASE Projeto_Avaliativo_Modulo_1_Viviane_Bueno;

-- Conecte-se à base de dados antes de executar os comandos abaixo

-- -----------------------------------------------------------------
-- CAMADA RAW (Dados brutos importados diretamente dos CSVs)
-- -----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.raw_viagem (
    id_viagem TEXT,
    num_proposta TEXT,
    situacao TEXT,
    viagem_urgente TEXT,
    cod_orgao_superior TEXT,
    nome_orgao_superior TEXT,
    cod_orgao_solicitante TEXT,
    nome_orgao_solicitante TEXT,
    cpf_viajante TEXT,
    nome_viajante TEXT,
    cargo TEXT,
    funcao TEXT,
    descricao_funcao TEXT,
    data_inicio TEXT,
    data_fim TEXT,
    destinos TEXT,
    motivo TEXT,
    valor_diarias TEXT,
    valor_passagens TEXT,
    valor_devolucao TEXT,
    valor_outros_gastos TEXT
);

CREATE TABLE IF NOT EXISTS public.raw_pagamento (
    id_viagem TEXT,
    cartao TEXT,
    data_pagamento TEXT,
    valor TEXT
);

CREATE TABLE IF NOT EXISTS public.raw_passagem (
    id_viagem TEXT,
    meio_transporte TEXT,
    tipo_passagem TEXT,
    valor_passagem TEXT,
    taxa_servico TEXT,
    desconto TEXT,
    valor_liquido TEXT
);

CREATE TABLE IF NOT EXISTS public.raw_trecho (
    id_viagem TEXT,
    origem TEXT,
    destino TEXT,
    data_partida TEXT,
    data_chegada TEXT
);

-- -----------------------------------------------------------------
-- CAMADA SILVER (Dados transformados e limpos)
-- -----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.silver_viagem AS SELECT * FROM public.raw_viagem WHERE 1=0;
CREATE TABLE IF NOT EXISTS public.silver_pagamento AS SELECT * FROM public.raw_pagamento WHERE 1=0;
CREATE TABLE IF NOT EXISTS public.silver_passagem AS SELECT * FROM public.raw_passagem WHERE 1=0;
CREATE TABLE IF NOT EXISTS public.silver_trecho AS SELECT * FROM public.raw_trecho WHERE 1=0;