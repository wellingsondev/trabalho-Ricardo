import streamlit as st
import pandas as pd
from datetime import datetime
from enum import Enum

# --- DEFINIÇÃO DAS CLASSES (Conforme Diagrama de Classes) ---

class enuFormaPagamento(Enum):
    DINHEIRO = "Dinheiro"
    CARTAO_CREDITO = "Cartão de Crédito"
    CARTAO_DEBITO = "Cartão de Débito"
    TICKET_ALIMENTACAO = "Ticket Alimentação"
    TICKET_REFEICAO = "Ticket Refeição"
    PIX = "Pix"

class Gasto:
    def __init__(self, tipo_gasto: str, data: datetime.date, valor: float, forma_pagamento: enuFormaPagamento):
        # RF01, RF02 e RF03 - Registro individual de gasto com data, valor e forma de pagamento 
        self.tipoGasto = tipo_gasto
        self.data = data
        self.valor = round(valor, 2) # RNF01 - Precisão decimal 
        self.formaPagamento = forma_pagamento

class ControleFinanceiro:
    def __init__(self, propriedade: str):
        self.propriedade = propriedade
        self.listaGasto = [] # Atributo derivado/lista de gastos 

    def adicionarGasto(self, gasto: Gasto):
        self.listaGasto.append(gasto)

    def gerarRelatorioMensal(self):
        # RF04 - Geração de relatório consolidado [cite: 13]
        if not self.listaGasto:
            return None
        return pd.DataFrame([
            {
                "Tipo": g.tipoGasto,
                "Data": g.data,
                "Valor": g.valor,
                "Forma de Pagamento": g.formaPagamento.value
            } for g in self.listaGasto
        ])

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="Controle de Gastos - Vera", layout="wide")
st.title("💰 Controle de Gastos Diários")

# Inicialização do estado da sessão para persistir os dados
if 'controle' not in st.session_state:
    st.session_state.controle = ControleFinanceiro("Vera")

controle = st.session_state.controle

# Sidebar - Cadastro (RF01, RF02, RF03)
st.sidebar.header("📝 Cadastrar Novo Gasto")
with st.sidebar.form("form_gasto"):
    tipo = st.text_input("Tipo do Gasto (Ex: Remédio, Roupa)")
    data_gasto = st.date_input("Data do Gasto", value=datetime.now())
    valor_gasto = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
    forma = st.selectbox("Forma de Pagamento", [e.value for e in enuFormaPagamento])
    
    if st.form_submit_button("Registrar Gasto"):
        if tipo and valor_gasto > 0:
            forma_enum = next(e for e in enuFormaPagamento if e.value == forma)
            novo_gasto = Gasto(tipo, data_gasto, valor_gasto, forma_enum)
            controle.adicionarGasto(novo_gasto)
            st.success("Gasto registrado!")
        else:
            st.error("Preencha todos os campos corretamente.")

# Área Principal - Visualização e Relatórios
tab1, tab2 = st.tabs(["📋 Listagem Geral", "📊 Relatórios Consolidados"])

with tab1:
    st.subheader("Histórico de Transações")
    df = controle.gerarRelatorioMensal()
    
    if df is not None:
        # RNF02 - Ordenação de dados 
        col_ordem = st.selectbox("Ordenar por:", ["Data", "Valor", "Tipo"])
        df = df.sort_values(by=col_ordem, ascending=(col_ordem == "Data"))
        st.dataframe(df.style.format({"Valor": "R$ {:.2f}"}), use_container_width=True)
    else:
        st.info("Nenhum gasto cadastrado ainda.")

with tab2:
    if df is not None:
        # RF05 - Agrupar total por categoria (tipo) [cite: 14]
        st.subheader("Total por Categoria")
        resumo_tipo = df.groupby("Tipo")["Valor"].sum().reset_index()
        st.table(resumo_tipo.style.format({"Valor": "R$ {:.2f}"}))

        # RF06 - Detalhar total por modalidade dentro de cada categoria [cite: 15]
        st.subheader("Detalhamento por Forma de Pagamento")
        detalhamento = df.groupby(["Tipo", "Forma de Pagamento"])["Valor"].sum().reset_index()
        st.dataframe(detalhamento.style.format({"Valor": "R$ {:.2f}"}), use_container_width=True)
        
        # Resumo visual simples
        st.metric("Gasto Total Acumulado", f"R$ {df['Valor'].sum():.2f}")
    else:
        st.info("Cadastre gastos para visualizar os relatórios.")