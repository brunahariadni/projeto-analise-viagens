# Análise de Despesas com Viagens Governamentais – 2025

## Sobre o projeto

Este projeto tem como objetivo analisar as despesas relacionadas às viagens realizadas por agentes públicos no ano de 2025, utilizando dados públicos disponibilizados pelo Governo Federal.

A proposta é aplicar conceitos de análise e tratamento de dados, modelagem e consultas SQL, além de utilizar Python para explorar os dados e gerar informações relevantes.

Link do Github: https://github.com/brunahariadni/projeto-analise-viagens

## Objetivos

- Organizar e estruturar os dados disponibilizados.
- Realizar o tratamento e a limpeza das informações.
- Construir consultas SQL para exploração dos dados.
- Identificar padrões e informações relevantes sobre as despesas.
- Desenvolver análises e visualizações para facilitar a interpretação dos resultados.

## Tecnologias utilizadas

- **MySQL:** armazenamento, organização e consultas aos dados.
- **MySQL Workbench:** gerenciamento do banco de dados e execução de consultas SQL.
- **Python:** tratamento e manipulação dos dados.
- **Pandas:** exploração e análise dos dados.
- **Matplotlib:** criação de gráficos e visualizações.
- **Jupyter Notebook:** desenvolvimento das análises.

## Fonte dos dados

Os dados utilizados são referentes às despesas com viagens governamentais do ano de 2025, obtidos por meio dos dados abertos do Governo Federal.

Os arquivos são disponibilizados em formato CSV e organizados em um arquivo ZIP para facilitar a obtenção e a importação.

## Estrutura do projeto

```text
projeto_viagens/
│
├── data/
│   └── Arquivos CSV e ZIP baixados
│
├── sql/
│   ├── 0_criar_banco.sql
│   ├── 2_validar_quantidades.sql
│   ├── 3_validar_dados.sql
│   ├── 4_criar_view_gold.sql
│   └── 5_criar_gold.sql
│
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
├── banco.py
├── config.py
│
├── teste_conexao.py
├── verificar_motivo.py
├── verificar_tamanhos.py
│
├── .gitignore
├── env.example
├── README.md
└── requirements.txt
```

**Observação:** os arquivos `.env`, `.venv` e `__pycache__` são utilizados localmente e não devem ser enviados ao GitHub. Os arquivos CSV e ZIP também são mantidos localmente e não fazem parte do versionamento.

## Etapas do desenvolvimento

1. **Coleta dos dados:** obtenção dos arquivos disponibilizados em dados abertos.
2. **Armazenamento (Raw):** criação do banco de dados e importação dos arquivos CSV para as tabelas Raw, preservando os dados originais.
3. **Tratamento (Silver):** limpeza, conversão de tipos, padronização e preparação dos dados por meio de Python e SQL.
4. **Validação:** verificação das quantidades de registros e análise de possíveis inconsistências.
5. **Consolidação (Gold):** criação de uma view e de uma tabela consolidada com indicadores agrupados por órgão superior.
6. **Análise exploratória:** utilização de Python, Pandas e Matplotlib para explorar os dados e desenvolver visualizações.

## Organização das camadas de dados

O projeto utiliza uma estrutura de três camadas:

- **Raw:** armazenamento dos dados originais importados dos arquivos CSV.
- **Silver:** dados tratados, padronizados e organizados em tabelas relacionais.
- **Gold:** dados consolidados e preparados para facilitar a análise dos indicadores.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd projeto_viagens
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

Ativar o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as credenciais

Copiar o arquivo `env.example`, renomear a cópia para `.env` e preencher as informações de conexão com o MySQL.

### 5. Criar o banco de dados

No MySQL Workbench, executar o arquivo:

`sql/0_criar_banco.sql`

**Atenção:** esse script recria as estruturas Raw e Silver e apaga tabelas existentes com esses nomes. Deve ser executado somente na preparação de um banco novo.

### 6. Extrair e importar os dados

Executar no terminal:

```bash
python 1_extrair.py
```

O script realiza o download dos arquivos, a extração dos CSVs e a importação dos dados para as tabelas Raw.

### 7. Transformar os dados

Executar:

```bash
python 2_transformar.py
```

O script realiza a limpeza, padronização e transformação dos dados, carregando as tabelas Silver.

**Atenção:** esse processo limpa e reconstrói as tabelas Silver antes de inserir os dados tratados.

### 8. Validar os dados

No MySQL Workbench, executar os arquivos:

- `sql/2_validar_quantidades.sql`
- `sql/3_validar_dados.sql`

Essas consultas permitem verificar as quantidades de registros e identificar possíveis inconsistências nos dados tratados.

### 9. Criar a camada Gold

Executar no MySQL Workbench, nesta ordem:

1. `sql/4_criar_view_gold.sql`
2. `sql/5_criar_gold.sql`

Esses scripts criam a view de consolidação e a tabela Gold com indicadores agrupados por órgão superior.

### 10. Executar as análises

Abrir o arquivo `3_analise.ipynb` no Jupyter Notebook e executar as células para explorar os dados e visualizar os resultados.

## Resultados

Os resultados e indicadores obtidos são apresentados por meio de consultas SQL, análises exploratórias e visualizações desenvolvidas durante o projeto.

A camada Gold reúne indicadores como quantidade de viagens, custo total, custo médio, pagamentos, passagens e trechos por órgão superior, facilitando a exploração e interpretação das informações.

## Autora

Bruna

Estudante de Análise e Desenvolvimento de Sistemas.