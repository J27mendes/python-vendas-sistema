# 📊 Sistema de Gerador de Relatórios e Análise de Dados

`Projeto Escolhido: 3. Gerador de Relatórios e Análise de Dados`

`Este projeto é um sistema de gerenciamento e análise de vendas implementado em Python, utilizando o banco de dados SQLite e seguindo uma arquitetura modular baseada nos princípios de Orientação a Objetos, Herança e Injeção de Dependência (DI).`

## 🚀 Requisitos e Funcionalidades

`O objetivo principal do sistema é gerenciar dados de Produtos e Vendas, além de gerar relatórios agregados complexos.`

### Funcionalidades Implementadas (Menu Principal)

O sistema oferece um menu interativo com as seguintes operações:

1. Buscar Produtos: Consulta interativa de produtos.

2. Atualizar Produto: Edição de dados de um produto existente.

3. Ver Vendas: Consulta interativa de registros de vendas.

4. Registrar Venda: Lançamento de novos registros de vendas.

5. Atualizar Venda: Edição de dados de uma venda existente.

6. Deletar Venda: Exclusão de um registro de venda pelo ID.

7. Imprimir Relatórios: Geração dos relatórios de análise de dados.

### Relatórios de Análise (Requisitos do Projeto)

`O sistema utiliza consultas SQL complexas (WHERE, ORDER BY, GROUP BY, INNER JOIN) para gerar os seguintes relatórios, conforme o requisito do projeto:`

✔️ Total de vendas por produto (SUM).

✔️ Média de preço de produtos (AVG).

✔️ Produtos mais/menos vendidos (ORDER BY + LIMIT).

✔️ Vendas por categoria (GROUP BY).

### 🧱 Arquitetura e Estrutura do Código

A arquitetura do projeto é altamente modular e coesa, com separação de responsabilidades em camadas:

| **Camada**         | **Arquivos (Exemplos)**                  | **Responsabilidade Principal**                                                                                                                             |
| ------------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model**          | Produto.py, Venda.py                     | Define as classes de dados e herda de `BaseModel`.                                                                                                         |
| **Repository**     | ProdutoRepository.py, VendaRepository.py | Responsável pela comunicação direta com o banco de dados (vendas.db). Implementa a herança de `BaseRepository` e o padrão de repositório genérico.         |
| **Service**        | ProdutoService.py, VendaService.py       | Contém a lógica de negócio (cálculos, validações). Utiliza Injeção de Dependência (DI), recebendo as instâncias de Repositório como argumento nos métodos. |
| **Controller**     | menu_views.py                            | Interage com o usuário (I/O) e coordena as chamadas para a camada Service.                                                                                 |
| **Infraestrutura** | Database.py, BaseRepository.py           | Gerencia a conexão com o SQLite e define métodos genéricos de CRUD (Herança).                                                                              |

`se preferir pode ver a estrutura como imagem`
**Estrutura do projeto** (Veja o diagrama de [estrutura de pastas](docs/estrutura_de_pastas.png)): |

### Padrões Chave Utilizados

**Herança:** Utilizada extensivamente nos Models (BaseModel) e nos Repositórios (BaseRepository), promovendo reuso de código e métodos CRUD genéricos.

**Banco de Dados:** SQLite (vendas.db) para persistência de dados.

**Modularização e Coesão:** Código dividido em módulos específicos (controllers, services, repositories, models), garantindo alta coesão e baixo acoplamento.

**Testes Unitários (Mocks e DI):** Testes na pasta tests/ utilizam unittest e unittest.mock para simular o comportamento dos Repositórios (usando DI) e garantir que a lógica dos Services esteja correta.

## ⚙️ Como Executar o Projeto

`Pré-requisitos`

`Certifique-se de ter o Python 3.8+ instalado. Não há dependências externas (o projeto usa o módulo sqlite3 nativo do Python).`

**Execução do Sistema** Navegue até a raiz do projeto:

Execute o arquivo principal:

🡆 python -m src.main 🡄

O sistema será iniciado, e o menu principal será exibido, permitindo que você interaja com o sistema.

## 🧪 Como Rodar os Testes Unitários

Os testes unitários (TestVendas.py) garantem a funcionalidade da camada Service, utilizando mocks para simular o Repositório e garantir a Injeção de Dependência.

**Execute o módulo unittest:** Navegue até a raiz do projeto (se ainda não estiver lá).
Execute o arquivo de teste:

🡆 python -m unittest src.tests.testVendas 🡄

O resultado deve exibir ... (indicando que os três testes passaram) seguido por OK.

### para melhor visualização dos relatórios em csv

É recomendado instalar a extensão: **Rainbow CSV** no seu VScode
