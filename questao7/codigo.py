import streamlit as st
import pandas as pd
from datetime import datetime

# --- CLASSES (Baseadas no Diagrama de Classe) ---

class Produto:
    def __init__(self, nome, unidade, qtd_mes, preco_estimado):
        # RF01 - Cadastro com nome, unidade, quantidade prevista e preço [cite: 19]
        self.nome = nome
        self.unidade = unidade
        self.qtdMes = float(qtd_mes) # RNF01 - Suporte a decimais 
        self.qtdCompra = float(qtd_mes) # RF02 - Inicialmente igual à prevista 
        self.precoEstimado = float(preco_estimado) # RNF01 - Suporte a decimais 

    def atualizarPrecoEstimado(self, novo_preco):
        # RF03 - Atualização do preço estimado [cite: 21]
        self.precoEstimado = float(novo_preco)

    def calcularTotalItem(self):
        # RF04 - Cálculo do subtotal do produto [cite: 22]
        return self.qtdCompra * self.precoEstimado

class ListaCompra:
    def __init__(self, mes_referenciado):
        self.mesReferenciado = mes_referenciado
        self.produtos = [] # Atributo derivado da relação 1..*

    def adicionarProduto(self, produto):
        self.produtos.append(produto)

    def CalcularTotalCompra(self):
        # RF05 - Cálculo do valor total geral da lista [cite: 23]
        return sum(p.calcularTotalItem() for p in self.produtos)

# --- CONFIGURAÇÃO DA INTERFACE (RNF03) --- 

st.set_page_config(page_title="Lista de Compras Mensal", layout="wide")

# Inicialização do estado da sessão (Persistência RNF02) 
if 'minha_lista' not in st.session_state:
    st.session_state.minha_lista = ListaCompra(datetime.now().strftime("%m/%Y"))

lista = st.session_state.minha_lista

st.title(f"🛒 Lista de Compras Mensal - {lista.mesReferenciado}")

# --- FORMULÁRIO DE CADASTRO (RF01) --- [cite: 19]
with st.expander("➕ Adicionar Novo Produto"):
    with st.form("novo_produto"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome do Produto")
        unid = col2.text_input("Unidade (ex: Kg, Un, Litro)")
        qtd_p = col1.number_input("Quantidade Prevista (Mês)", min_value=0.0, step=0.1)
        preco_e = col2.number_input("Preço Estimado (R$)", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Cadastrar"):
            if nome:
                novo = Produto(nome, unid, qtd_p, preco_e)
                lista.adicionarProduto(novo)
                st.success(f"{nome} adicionado!")
                st.rerun()

# --- TABELA DE CONFERÊNCIA (RNF03 / RF02 / RF03 / RF04) --- [cite: 20, 21, 22, 26]
if lista.produtos:
    st.subheader("📝 Itens da Lista")
    
    # Criando uma estrutura para edição manual
    for i, prod in enumerate(lista.produtos):
        col_nome, col_qtd, col_preco, col_sub = st.columns([3, 2, 2, 2])
        
        with col_nome:
            st.write(f"**{prod.nome}** ({prod.unidade})")
            st.caption(f"Previsto: {prod.qtdMes}")
            
        with col_qtd:
            # RF02 - Edição manual da quantidade efetiva 
            prod.qtdCompra = st.number_input(f"Qtd Compra", value=prod.qtdCompra, 
                                            key=f"qtd_{i}", step=0.1, label_visibility="collapsed")
            
        with col_preco:
            # RF03 - Atualização mensal do preço estimado [cite: 21]
            novo_p = st.number_input(f"Preço", value=prod.precoEstimado, 
                                     key=f"prc_{i}", step=0.01, label_visibility="collapsed")
            prod.atualizarPrecoEstimado(novo_p)
            
        with col_sub:
            # RF04 - Exibição do subtotal [cite: 22]
            st.write(f"R$ {prod.calcularTotalItem():.2f}")
        
        st.divider()

    # --- TOTAL GERAL (RF05) --- [cite: 23]
    total_geral = lista.CalcularTotalCompra()
    st.markdown(f"## **Total Geral Estimado: R$ {total_geral:.2f}**")

else:
    st.info("Nenhum produto cadastrado na lista.")

# Opção para resetar a lista para o mês seguinte (Simulação RNF02) 
if st.sidebar.button("Limpar Lista para Novo Mês"):
    st.session_state.minha_lista = ListaCompra(datetime.now().strftime("%m/%Y"))
    st.rerun()