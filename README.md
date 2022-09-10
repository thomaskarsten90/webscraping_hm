
![Dashboard](https://github.com/thomaskarsten90/webscraping_hm/blob/cf953b73a021e89155f7a64c1945b5f13a9b784d/Dashboard_hm_project.png)

# A empresa Star Jeans!

## PROBLEMA DO NEGÓCIO:
    Uma empresa brasileira (fictícia) deseja entrar no mercado de moda americano. Mais especificamente, montar um e-commerce 
    para vendas de calças jeans masculinas.
    
    O objetivo é manter o custo de operação baixo e escalar a medida que forem conseguindo clientes.
    
    Além de ter o produto de entrada e a audiência definidos, a contratante deseja ter uma visão do mercado americano 
    neste segmento, para poder definir os preços dos seu produtos. 
    
    A empresa Star Jeans considera que o seu principal concorrente é a H&M, uma empresa americana (real) de grande 
    porte no ramo da moda.
    
    Assim, a empresa brasileira contrata uma consultoria de Ciência de Dados para responder as seguintes perguntas: 
        1. Qual o preço de venda médio das calças de cada modelo e cor anunciado no site da H&M? 
        2. Quantos tipos de calças e cores o principal concorrente anuncia em seu site? 
        3. Quais as matérias-prima necessárias para confeccionar as calças?

# Quais foram as etapas para a confecção deste projeto?
## Método CRISP-DS de desenvolvimento:
![CRISP](https://github.com/thomaskarsten90/webscraping_hm/blob/cf953b73a021e89155f7a64c1945b5f13a9b784d/metodo_CRISP.png)

## 1.0. - Etapas do Pensamento analítico:
    1.1. Identificação da causa raíz;
    1.2. Definir um escopo fechado para uma pergunta aberta;
    1.3. Quebrar o problema definido em tarefas menores;
    1.4. Organizar as tarefas por ordem lógica;
    1.5. Executar com uma mentalidade cíclica.

## 2.0. - Questão de negócio: Qual o preço de venda médio das calças de cada modelo e cor anunciado no site da H&M?
    2.1. Identificação da causa raiz:
        - Motivação: Qual o contexto?
            - A empresa está entratando no mercado de varejo de moda dos USA e não tem experiência no mercado americano;
            - Definir a média de preço do produdo para gerar insights.
         - Qual é a causa raíz do problema?
            - Precificação do produto;
            - Preço ótimo para maximizar o lucro:
    2.2. Definir um escopo fechado para uma pergunta aberta.
            - Pergunta aberta: Qual o preço de venda médio das calças de cada modelo e cor anunciado no site da H&M?
            - Escopo fechado: Produto | Tempo | Localidade | Atributos do Produto. 
                - Media dos preços dos sites concorrentes por produto, tipo e cor dos últimos 30 dias. 
    2.3. Quebrar o problema definido em tarefas menores:
        - Media dos preços dos sites concorrentes por produto, tipo e cor dos últimos 30 dias.

         Tarefas:
            - Calcular a media de preços dos sites concorrentes por produto, tipo e cor dos últimos 30 dias;
            - Montar uma base de dados que contenha informações do produto, preço, tipo, cor, dias de exposição;
            - Definir o Schema (colunas da tabale);
            - Definir a infraestrutura (banco de dados, csv, API);
            - Desegin do ETL;
            - Agendamento da atualização da tabela;
            - Entrega do produto final.

    2.4. Organizar as tarefas por ordem lógica:
        1. Montar uma base de dados que contenha informações do produto, preço, tipo, cor, dias de exposição;
        2. Definir o Schema;
        3. Definir a infraestrutura;
        4. Fazer o ETL;
        5. Calcular a mediana de preços dos sites concorrentes por produto, tipo e cor dos últimos 30 dias;
        6. Fazer a visualização do produto final (tabela, gráfico);
        7. Entregar o produto final.
    
    2.5. Executar com uma mentalidade cíclica.
        1. Preciso passar por todas tarefas o mais rápido possível para:
            1. Identificar bloqueios;
            2. Identificar impeditivos que possam desvalidar o projeto;
            3. Entregar o valor para empresa rapidamente. 
        2. Fazer escolhas simples (keep it simple)

## 3.0. - Etapas de um projeto de dados:
    1. Questão do negócio;
    2. Entendimento do negócio;
    3. Coleta de dados;
    4. Limpeza de dados;
    5. Exploração de dados;
    6. Modelagem de dados;
    7. Aplicação dos algorítmos de Machine Learning;
    8. Avaliação de performance dos algorítmos;
    9. Publicação do modelo em Produção.  

# 4.0. - Resumo do projeto:

  Após ter sido estudado a questão do negócio, fiz o entendimento do negócio estudando as principais métricas de um modelo de negócio e-commerce. 
  Com isso em mente, crei um banco de dados e fiz a coleta dos dados utilizando a biblioteca BeautifulSoup.
  Automatizei o processo de webscraping através do crontab e deixei coletando por alguns dias. Após a coleta, já com os dados limpos, 
explorados e modelados, utilizei o PowerBI para criar uma visualização dos resultados obtidos no projeto.

        2. Ferramentas 
            - Python 3.9.12;
            - Biblioteca de Webscrapping (BS4);
            - Sqlite3
            - VSCODE;
            - Crontjob;
            - PowerBI.
