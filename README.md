# Projeto_Avaliativo_Modulo_1_Viviane_Bueno
# Projeto Avaliativo - Módulo 1: Pipeline ETL e Análise de Dados de Viagens

Repositório desenvolvido para o projeto avaliativo do módulo 1, aplicando os conceitos de Engenharia de Dados (Arquitetura Medallion), modelagem relacional em PostgreSQL e análise exploratória com Python.

---

## 🚀 Sobre o Projeto
O objetivo deste projeto é processar, transformar e analisar dados públicos de viagens a serviço da administração pública federal. A solução contempla a criação de um banco de dados relacional robusto e a extração de insights estratégicos de negócio através de visualizações gráficas.

## 🗂️ Arquitetura e Estruturação
O projeto segue o conceito de **Arquitetura Medallion**:
* **Raw (Camada Crua):** Ingestão inicial dos arquivos CSV brutos de viagens, pagamentos e trechos.
* **Silver (Camada Limpa):** Tabelas estruturadas no PostgreSQL com chaves primárias, estrangeiras e tratamento de tipos de dados.
* **Gold (Camada de Negócio / Análise):** Consultas e transformações avançadas em Python (`Pandas`) para responder às perguntas de negócio.

---

## 📊 Principais Insights e Perguntas de Negócio
O notebook `3_analise.ipynb` responde a 7 perguntas estratégicas:
1. **Top 5 Órgãos:** Órgãos superiores com maior custo total em viagens.
2. **Custo Médio por Destino:** Os destinos com maiores médias de custo por viagem.
3. **Viagem de Maior Duração:** Identificação do processo mais longo e seu custo associado.
4. **Tipos de Pagamento:** Análise dos meios de pagamento com maior valor médio.
5. **Meios de Transporte:** Frequência de utilização de cada modalidade nos trechos.
6. **UFs de Destino:** Estados que concentram o maior volume de trechos de viagens.
7. **Órgão Pagador:** O órgão com o maior montante financeiro despendido.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python
* **Banco de Dados:** PostgreSQL
* **Bibliotecas Python:** Pandas, SQLAlchemy, Matplotlib, Seaborn
* **Controle de Versão:** Git / GitHub

---
**Desenvolvido por:** Viviane Bueno
