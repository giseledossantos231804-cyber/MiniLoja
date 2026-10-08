# 📦 Controle de Estoque — TechStore

## O que é
Sistema de controle de estoque para a loja fictícia **TechStore** (eletrônicos), feito em Python com interface web usando Streamlit.

## Objetivo
Material de aprendizagem para iniciantes: praticar variáveis, listas, dicionários, `if/elif/else`, laços `for`/`while` e funções em um projeto real e visual.

## Tecnologias
- Python 3.9+
- Streamlit (interface)
- Pandas (apenas para o gráfico do dashboard)

## Como instalar
```bash
cd controle_estoque
python -m venv venv
# Windows:  venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## Como executar
```bash
streamlit run app.py
```
O navegador abrirá em `http://localhost:8501`.

## Como usar
| Menu | O que faz |
|---|---|
| Dashboard | Indicadores e gráfico de produtos por categoria |
| Cadastrar Produto | Adiciona um produto novo |
| Visualizar Estoque | Tabela com valor em estoque e situação |
| Pesquisar Produto | Busca pelo nome (ignora maiúsculas/minúsculas) |
| Entrada de Estoque | Soma unidades recebidas |
| Saída de Estoque | Retira unidades (bloqueia se passar do disponível) |
| Excluir Produto | Remove um produto, com confirmação |

Situação: 🟢 normal (mais de 5) · 🟡 baixo (1 a 5) · 🔴 zerado (0).

> ⚠️ Os dados ficam só na memória. Ao fechar o programa (ou recarregar a página), voltam aos produtos iniciais.

## Estrutura
```text
controle_estoque/
├── app.py            # todo o código do sistema
├── requirements.txt  # dependências
└── README.md         # este arquivo
```

## Melhorias futuras
- **V2:** visual melhor, filtros, mais gráficos, edição de produtos
- **V3:** salvar em CSV/Excel
- **V4:** SQLite, login, níveis de acesso, histórico de movimentações
- **V5:** publicar na internet e deixar a interface mais profissional
