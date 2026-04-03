import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# Inicialização dos dados
# -----------------------------
if "contas" not in st.session_state:
    st.session_state.contas = []

# -----------------------------
# Classe ContaLuz
# -----------------------------
class ContaLuz:
    def __init__(self, dtLeitura, nLeitura, kwGasto, valorPagar, dataPagamento):
        self.dtLeitura = dtLeitura
        self.nLeitura = nLeitura
        self.kwGasto = kwGasto
        self.valorPagar = valorPagar
        self.dataPagamento = dataPagamento

    def to_dict(self):
        return {
            "Data Leitura": self.dtLeitura,
            "Nº Leitura": self.nLeitura,
            "KW Gasto": self.kwGasto,
            "Valor Pagar": self.valorPagar,
            "Data Pagamento": self.dataPagamento
        }

# -----------------------------
# Funções
# -----------------------------
def calcular_media():
    if len(st.session_state.contas) == 0:
        return 0
    total = sum(c.kwGasto for c in st.session_state.contas)
    return total / len(st.session_state.contas)

def calcular_menor():
    if len(st.session_state.contas) == 0:
        return None
    return min(st.session_state.contas, key=lambda c: c.kwGasto)

def calcular_maior():
    if len(st.session_state.contas) == 0:
        return None
    return max(st.session_state.contas, key=lambda c: c.kwGasto)

# -----------------------------
# Interface
# -----------------------------
st.title("💡 Sistema de Conta de Luz")

menu = st.sidebar.selectbox("Menu", [
    "Cadastrar Conta",
    "Listar Contas",
    "Estatísticas",
    "Atualizar Conta"
])

# -----------------------------
# CADASTRAR
# -----------------------------
if menu == "Cadastrar Conta":
    st.subheader("➕ Cadastro de Conta")

    dtLeitura = st.date_input("Data da Leitura")
    nLeitura = st.number_input("Número da Leitura", min_value=0)
    kwGasto = st.number_input("KW Gasto", min_value=0.0)
    valorPagar = st.number_input("Valor a Pagar", min_value=0.0)
    dataPagamento = st.date_input("Data de Pagamento")

    if st.button("Cadastrar"):
        conta = ContaLuz(dtLeitura, nLeitura, kwGasto, valorPagar, dataPagamento)
        st.session_state.contas.append(conta)
        st.success("Conta cadastrada com sucesso!")

# -----------------------------
# LISTAR
# -----------------------------
elif menu == "Listar Contas":
    st.subheader("📋 Contas Cadastradas")

    if len(st.session_state.contas) == 0:
        st.warning("Nenhuma conta cadastrada.")
    else:
        df = pd.DataFrame([c.to_dict() for c in st.session_state.contas])
        st.dataframe(df)

# -----------------------------
# ESTATÍSTICAS
# -----------------------------
elif menu == "Estatísticas":
    st.subheader("📊 Estatísticas")

    if len(st.session_state.contas) == 0:
        st.warning("Nenhum dado disponível.")
    else:
        media = calcular_media()
        menor = calcular_menor()
        maior = calcular_maior()

        st.write(f"📌 Média de Consumo: {media:.2f} KW")

        st.write("🔻 Menor Consumo:")
        st.write(f"{menor.kwGasto} KW - {menor.dtLeitura}")

        st.write("🔺 Maior Consumo:")
        st.write(f"{maior.kwGasto} KW - {maior.dtLeitura}")

# -----------------------------
# ATUALIZAR
# -----------------------------
elif menu == "Atualizar Conta":
    st.subheader("✏️ Atualizar Conta")

    if len(st.session_state.contas) == 0:
        st.warning("Nenhuma conta cadastrada.")
    else:
        index = st.selectbox("Selecione a conta", range(len(st.session_state.contas)))

        conta = st.session_state.contas[index]

        dtLeitura = st.date_input("Data Leitura", conta.dtLeitura)
        nLeitura = st.number_input("Número Leitura", value=conta.nLeitura)
        kwGasto = st.number_input("KW Gasto", value=conta.kwGasto)
        valorPagar = st.number_input("Valor Pagar", value=conta.valorPagar)
        dataPagamento = st.date_input("Data Pagamento", conta.dataPagamento)

        if st.button("Atualizar"):
            conta.dtLeitura = dtLeitura
            conta.nLeitura = nLeitura
            conta.kwGasto = kwGasto
            conta.valorPagar = valorPagar
            conta.dataPagamento = dataPagamento
            st.success("Conta atualizada com sucesso!")