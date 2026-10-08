# =====================================================
# TechStore - Sistema de Controle de Estoque
# Projeto didático para iniciantes em Python
# Para executar:  streamlit run app.py
# =====================================================

import streamlit as st
import pandas as pd  # usado só para montar o gráfico do dashboard

# -----------------------------------------------------
# PARTE 1 - CONFIGURAÇÕES E DADOS INICIAIS
# -----------------------------------------------------

st.set_page_config(page_title="TechStore - Estoque", page_icon="📦", layout="wide")

# Até esta quantidade (inclusive), o estoque é considerado baixo
LIMITE_ESTOQUE_BAIXO = 5

# Categorias disponíveis no cadastro
CATEGORIAS = ["Computadores", "Periféricos", "Imagem e Vídeo", "Armazenamento", "Acessórios"]


def criar_produtos_iniciais():
    """Devolve a lista de produtos de exemplo.
    Cada produto é um dicionário; a lista guarda todos eles."""
    return [
        {"id": 1,  "nome": "Notebook",    "categoria": "Computadores",   "preco": 3500.00, "quantidade": 8},
        {"id": 2,  "nome": "Mouse",       "categoria": "Periféricos",    "preco": 50.00,   "quantidade": 10},
        {"id": 3,  "nome": "Teclado",     "categoria": "Periféricos",    "preco": 120.00,  "quantidade": 18},
        {"id": 4,  "nome": "Monitor",     "categoria": "Imagem e Vídeo", "preco": 900.00,  "quantidade": 6},
        {"id": 5,  "nome": "Webcam",      "categoria": "Imagem e Vídeo", "preco": 250.00,  "quantidade": 4},
        {"id": 6,  "nome": "Headset",     "categoria": "Periféricos",    "preco": 200.00,  "quantidade": 12},
        {"id": 7,  "nome": "Impressora",  "categoria": "Periféricos",    "preco": 800.00,  "quantidade": 3},
        {"id": 8,  "nome": "Pen Drive",   "categoria": "Armazenamento",  "preco": 40.00,   "quantidade": 30},
        {"id": 9,  "nome": "HD Externo",  "categoria": "Armazenamento",  "preco": 400.00,  "quantidade": 0},
        {"id": 10, "nome": "Cabo HDMI",   "categoria": "Acessórios",     "preco": 25.00,   "quantidade": 5},
    ]


# O Streamlit executa o arquivo inteiro a cada clique. Por isso guardamos a lista
# em st.session_state: assim ela NÃO é recriada do zero a cada clique.
if "produtos" not in st.session_state:
    st.session_state["produtos"] = criar_produtos_iniciais()

produtos = st.session_state["produtos"]  # atalho para usar a lista


# -----------------------------------------------------
# PARTE 2 - FUNÇÕES AUXILIARES
# -----------------------------------------------------

def formatar_moeda(valor):
    """Transforma 1234.5 em 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}"  # 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def buscar_produto_por_id(id_produto):
    """Procura um produto pelo id. Devolve o dicionário ou None."""
    for produto in produtos:
        if produto["id"] == id_produto:
            return produto
    return None


def gerar_novo_id():
    """Encontra o primeiro número de id que ainda não está em uso."""
    novo_id = 1
    while buscar_produto_por_id(novo_id) is not None:
        novo_id = novo_id + 1
    return novo_id


def situacao_produto(quantidade):
    """Diz se o estoque está normal, baixo ou zerado."""
    if quantidade == 0:
        return "🔴 Estoque zerado"
    elif quantidade <= LIMITE_ESTOQUE_BAIXO:
        return "🟡 Estoque baixo"
    else:
        return "🟢 Estoque normal"


# -----------------------------------------------------
# PARTE 3 - FUNÇÕES DO SISTEMA (regras de negócio)
# Elas devolvem (True/False, mensagem) para a tela mostrar o resultado.
# -----------------------------------------------------

def cadastrar_produto(nome, categoria, preco, quantidade):
    """Valida os dados e adiciona um novo produto à lista."""
    nome = nome.strip()  # remove espaços sobrando

    if nome == "":
        return False, "Erro: o nome do produto não pode ficar vazio."
    if preco <= 0:
        return False, "Erro: o preço deve ser maior que zero."
    for produto in produtos:
        if produto["nome"].lower() == nome.lower():
            return False, "Erro: já existe um produto com esse nome."

    novo_produto = {
        "id": gerar_novo_id(),
        "nome": nome,
        "categoria": categoria,
        "preco": preco,
        "quantidade": quantidade,
    }
    produtos.append(novo_produto)
    return True, "Produto cadastrado com sucesso!"


def listar_produtos(lista):
    """Monta as linhas da tabela a partir de uma lista de produtos."""
    linhas = []
    for produto in lista:
        valor_em_estoque = produto["preco"] * produto["quantidade"]
        linhas.append({
            "ID": produto["id"],
            "Produto": produto["nome"],
            "Categoria": produto["categoria"],
            "Preço": formatar_moeda(produto["preco"]),
            "Quantidade": produto["quantidade"],
            "Valor em estoque": formatar_moeda(valor_em_estoque),
            "Situação": situacao_produto(produto["quantidade"]),
        })
    return linhas


def pesquisar_produto(texto):
    """Devolve os produtos cujo nome contém o texto (sem diferenciar maiúsculas)."""
    texto = texto.strip().lower()
    encontrados = []
    for produto in produtos:
        if texto in produto["nome"].lower():
            encontrados.append(produto)
    return encontrados


def entrada_estoque(id_produto, quantidade):
    """Soma a quantidade recebida ao estoque do produto."""
    produto = buscar_produto_por_id(id_produto)
    if produto is None:
        return False, "Erro: produto não encontrado."
    if quantidade <= 0:
        return False, "Erro: a quantidade deve ser maior que zero."
    produto["quantidade"] = produto["quantidade"] + quantidade
    return True, f"Estoque atualizado: {produto['quantidade']}"


def saida_estoque(id_produto, quantidade):
    """Subtrai a quantidade do estoque, se houver unidades suficientes."""
    produto = buscar_produto_por_id(id_produto)
    if produto is None:
        return False, "Erro: produto não encontrado."
    if quantidade <= 0:
        return False, "Erro: a quantidade deve ser maior que zero."
    if quantidade > produto["quantidade"]:
        return False, "Erro: quantidade solicitada maior que o estoque disponível."
    produto["quantidade"] = produto["quantidade"] - quantidade
    return True, f"Estoque atualizado: {produto['quantidade']}"


def excluir_produto(id_produto):
    """Remove o produto da lista."""
    produto = buscar_produto_por_id(id_produto)
    if produto is None:
        return False, "Erro: produto não encontrado."
    produtos.remove(produto)
    return True, f"Produto '{produto['nome']}' excluído com sucesso!"


def calcular_total_estoque():
    """Soma preço x quantidade de todos os produtos."""
    total = 0
    for produto in produtos:
        total = total + produto["preco"] * produto["quantidade"]
    return total


def calcular_total_itens():
    """Soma as quantidades de todos os produtos."""
    total = 0
    for produto in produtos:
        total = total + produto["quantidade"]
    return total


def contar_estoque_baixo():
    """Conta produtos com estoque baixo ou zerado."""
    contador = 0
    for produto in produtos:
        if produto["quantidade"] <= LIMITE_ESTOQUE_BAIXO:
            contador = contador + 1
    return contador


def produtos_por_categoria():
    """Devolve um dicionário no formato {categoria: quantidade de produtos}."""
    contagem = {}
    for produto in produtos:
        categoria = produto["categoria"]
        if categoria in contagem:
            contagem[categoria] = contagem[categoria] + 1
        else:
            contagem[categoria] = 1
    return contagem


# -----------------------------------------------------
# PARTE 4 - TELAS (interface com Streamlit)
# -----------------------------------------------------

def escolher_produto(chave):
    """Mostra uma caixa de seleção e devolve o id do produto escolhido.
    Cada opção aparece assim: '2 - Mouse'."""
    opcoes = []
    for produto in produtos:
        opcoes.append(f"{produto['id']} - {produto['nome']}")
    escolhido = st.selectbox("Selecione o produto", opcoes, key=chave)
    return int(escolhido.split(" - ")[0])  # pega só o número do id


def tela_dashboard():
    st.subheader("📊 Dashboard")

    # 4 cards lado a lado
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total de produtos", len(produtos))
    col2.metric("🔢 Total de itens", calcular_total_itens())
    col3.metric("💰 Valor do estoque", formatar_moeda(calcular_total_estoque()))
    col4.metric("⚠️ Estoque baixo", contar_estoque_baixo())

    st.divider()
    st.subheader("Produtos por categoria")

    contagem = produtos_por_categoria()
    if len(contagem) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    # Transforma o dicionário em tabela para o gráfico
    tabela = pd.DataFrame({
        "Categoria": list(contagem.keys()),
        "Produtos": list(contagem.values()),
    }).set_index("Categoria")
    st.bar_chart(tabela)
    st.dataframe(tabela)


def tela_cadastrar():
    st.subheader("➕ Cadastrar Produto")

    with st.form("form_cadastro", clear_on_submit=True):
        nome = st.text_input("Nome do produto")
        categoria = st.selectbox("Categoria", CATEGORIAS)
        preco = st.number_input("Preço (R$)", min_value=0.0, step=0.01, format="%.2f")
        quantidade = st.number_input("Quantidade inicial", min_value=0, step=1)
        enviado = st.form_submit_button("Cadastrar Produto")

    if enviado:
        ok, mensagem = cadastrar_produto(nome, categoria, preco, int(quantidade))
        if ok:
            st.success(mensagem)
        else:
            st.error(mensagem)


def tela_visualizar():
    st.subheader("📋 Estoque")
    if len(produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return
    st.dataframe(listar_produtos(produtos), use_container_width=True, hide_index=True)


def tela_pesquisar():
    st.subheader("🔎 Pesquisar Produto")
    texto = st.text_input("Digite o nome do produto", placeholder="Ex.: mouse")

    if texto.strip() == "":
        st.info("Digite um nome para pesquisar.")
        return

    encontrados = pesquisar_produto(texto)
    if len(encontrados) == 0:
        st.warning("Nenhum produto encontrado.")
    else:
        st.dataframe(listar_produtos(encontrados), use_container_width=True, hide_index=True)


def tela_entrada():
    st.subheader("📥 Entrada de Estoque")
    if len(produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    id_produto = escolher_produto("select_entrada")
    produto = buscar_produto_por_id(id_produto)
    st.write(f"**Estoque atual:** {produto['quantidade']}")

    quantidade = st.number_input("Quantidade recebida", min_value=1, step=1, key="qtd_entrada")

    if st.button("Registrar Entrada"):
        ok, mensagem = entrada_estoque(id_produto, int(quantidade))
        if ok:
            st.success(mensagem)
        else:
            st.error(mensagem)


def tela_saida():
    st.subheader("📤 Saída de Estoque")
    if len(produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    id_produto = escolher_produto("select_saida")
    produto = buscar_produto_por_id(id_produto)
    st.write(f"**Estoque atual:** {produto['quantidade']}")

    quantidade = st.number_input("Quantidade solicitada", min_value=1, step=1, key="qtd_saida")

    if st.button("Registrar Saída"):
        ok, mensagem = saida_estoque(id_produto, int(quantidade))
        if ok:
            st.success(mensagem)
        else:
            st.error(mensagem)


def tela_excluir():
    st.subheader("🗑️ Excluir Produto")
    if len(produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    id_produto = escolher_produto("select_excluir")
    confirmou = st.checkbox("Sim, tenho certeza que quero excluir este produto")

    if st.button("Excluir Produto"):
        if confirmou:
            ok, mensagem = excluir_produto(id_produto)
            if ok:
                st.success(mensagem)
            else:
                st.error(mensagem)
        else:
            st.warning("Marque a caixa de confirmação antes de excluir.")


# -----------------------------------------------------
# PARTE 5 - PROGRAMA PRINCIPAL (cabeçalho + menu)
# -----------------------------------------------------

st.title("📦 Controle de Estoque")
st.caption("TechStore — Sistema de gerenciamento de produtos")

st.sidebar.title("Menu")
opcao = st.sidebar.radio("Escolha uma opção:", [
    "Dashboard",
    "Cadastrar Produto",
    "Visualizar Estoque",
    "Pesquisar Produto",
    "Entrada de Estoque",
    "Saída de Estoque",
    "Excluir Produto",
])

# Cada opção do menu chama a tela correspondente
if opcao == "Dashboard":
    tela_dashboard()
elif opcao == "Cadastrar Produto":
    tela_cadastrar()
elif opcao == "Visualizar Estoque":
    tela_visualizar()
elif opcao == "Pesquisar Produto":
    tela_pesquisar()
elif opcao == "Entrada de Estoque":
    tela_entrada()
elif opcao == "Saída de Estoque":
    tela_saida()
elif opcao == "Excluir Produto":
    tela_excluir()
