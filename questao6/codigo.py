import streamlit as st
import pandas as pd

# --- CLASSES DO SISTEMA (Baseadas no Diagrama de Classes e RFs) ---

class Produto:
    def __init__(self, id_prod, nome, valor):
        self.id = id_prod
        self.nome = nome
        self.valor = float(valor) # RNF01: Integridade dos preços

    def consultarPreco(self):
        return self.valor

class Comanda:
    def __init__(self, numeroComanda):
        # RF01: Abertura por numeração
        self.numeroComanda = int(numeroComanda)
        self.itensConsumidos = [] # Lista de dicionários {produto, quantidade}
        self.status = "Aberta"

    def registrarConsumo(self, produto, quantidade):
        # RF02: Registrar produtos e quantidades
        self.itensConsumidos.append({
            "produto": produto,
            "quantidade": quantidade
        })

    def valorTotal(self):
        # RF03 e RF04: Recuperar valor unitário e calcular soma total
        total = sum(item["produto"].consultarPreco() * item["quantidade"] 
                    for item in self.itensConsumidos)
        return total

class Caixa:
    def __init__(self):
        self.comandaAtual = None

    def lerComanda(self, comanda):
        self.comandaAtual = comanda
        return self.comandaAtual

    def finalizarCompra(self):
        if self.comandaAtual:
            self.comandaAtual.status = "Finalizada"
            return True
        return False

# --- CONFIGURAÇÃO E INTERFACE (RNF02: Resposta imediata) ---

st.set_page_config(page_title="Padaria Doce Sabor - Comandas", layout="wide")

# Inicialização do Banco de Dados em Memória
if 'produtos' not in st.session_state:
    st.session_state.produtos = [
        Produto(1, "Pão de Sal", 0.50),
        Produto(2, "Café com Leite", 4.50),
        Produto(3, "Bolo de Fubá (fatia)", 3.00),
        Produto(4, "Suco de Laranja", 6.00)
    ]

if 'comandas' not in st.session_state:
    st.session_state.comandas = {}

st.title("🥖 Padaria Doce Sabor - Gestão de Comandas")

menu = st.sidebar.selectbox("Operação", ["Atendimento", "Caixa (Fechamento)", "Cadastro de Produtos"])

# --- FUNCIONALIDADES ---

# RF01 e RF02 - Atendimento (Registro de Consumo)
if menu == "Atendimento":
    st.header("📝 Registro de Consumo")
    
    num_comanda = st.number_input("Número da Comanda", min_value=1, step=1)
    
    # Abrir ou recuperar comanda
    if num_comanda not in st.session_state.comandas:
        if st.button("Abrir Nova Comanda"):
            st.session_state.comandas[num_comanda] = Comanda(num_comanda)
            st.success(f"Comanda {num_comanda} aberta!")
    
    if num_comanda in st.session_state.comandas:
        comanda = st.session_state.comandas[num_comanda]
        if comanda.status == "Aberta":
            st.info(f"Comanda {num_comanda} está ATIVA.")
            
            with st.form("registro_produto"):
                prod_selecionado = st.selectbox("Produto", 
                    st.session_state.produtos, format_func=lambda x: f"{x.nome} - R$ {x.valor:.2f}")
                qtd = st.number_input("Quantidade", min_value=1, step=1)
                
                if st.form_submit_button("Adicionar à Comanda"):
                    comanda.registrarConsumo(prod_selecionado, qtd)
                    st.success(f"{qtd}x {prod_selecionado.nome} adicionado.")
        else:
            st.error("Esta comanda já foi finalizada no caixa.")

# RF03 e RF04 - Caixa (Fechamento de Comanda)
elif menu == "Caixa (Fechamento)":
    st.header("💰 Fechamento de Caixa")
    
    num_fechamento = st.number_input("Número da Comanda para Fechamento", min_value=1, step=1)
    
    if num_fechamento in st.session_state.comandas:
        comanda = st.session_state.comandas[num_fechamento]
        caixa = Caixa()
        caixa.lerComanda(comanda)
        
        st.subheader(f"Resumo Comanda #{num_fechamento}")
        
        if comanda.itensConsumidos:
            # Gerar tabela de resumo
            dados = []
            for item in comanda.itensConsumidos:
                dados.append({
                    "Item": item["produto"].nome,
                    "Qtd": item["quantidade"],
                    "Unitário": f"R$ {item['produto'].valor:.2f}",
                    "Subtotal": f"R$ {item['produto'].valor * item['quantidade']:.2f}"
                })
            st.table(pd.DataFrame(dados))
            
            total = comanda.valorTotal()
            st.markdown(f"### **VALOR TOTAL: R$ {total:.2f}**")
            
            if comanda.status == "Aberta":
                if st.button("Finalizar Compra e Receber Pagamento"):
                    if caixa.finalizarCompra():
                        st.balloons()
                        st.success("Pagamento confirmado! Comanda finalizada.")
            else:
                st.warning("Esta comanda já consta como PAGA.")
        else:
            st.warning("Esta comanda não possui itens registrados.")
    else:
        st.error("Comanda não encontrada.")

# Cadastro de Produtos (Gestão do Atributo Produto)
elif menu == "Cadastro de Produtos":
    st.header("🥐 Gestão de Cardápio")
    with st.form("novo_prod"):
        nome_p = st.text_input("Nome do Produto")
        preco_p = st.number_input("Preço Unitário", min_value=0.0, format="%.2f")
        if st.form_submit_button("Cadastrar Produto"):
            novo_id = len(st.session_state.produtos) + 1
            st.session_state.produtos.append(Produto(novo_id, nome_p, preco_p))
            st.success("Produto cadastrado com sucesso!")
    
    st.write("### Produtos Atuais")
    st.table(pd.DataFrame([{"ID": p.id, "Nome": p.nome, "Preço": f"R$ {p.valor:.2f}"} 
                           for p in st.session_state.produtos]))