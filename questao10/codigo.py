import streamlit as st
from datetime import date

st.title("📅 Sistema de Sala de Reunião")

# ----------------------------
# Inicialização dos dados
# ----------------------------
if "salas" not in st.session_state:
    st.session_state.salas = []

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = []

if "reunioes" not in st.session_state:
    st.session_state.reunioes = []

# ----------------------------
# CADASTRO DE SALAS
# ----------------------------
st.header("🏢 Cadastro de Salas")

with st.form("form_sala"):
    numero = st.number_input("Número da sala", min_value=1)
    capacidade = st.number_input("Capacidade", min_value=1)
    submit_sala = st.form_submit_button("Cadastrar Sala")

    if submit_sala:
        st.session_state.salas.append({
            "numero": numero,
            "capacidade": capacidade
        })
        st.success("Sala cadastrada!")

# ----------------------------
# CADASTRO DE FUNCIONÁRIOS
# ----------------------------
st.header("👤 Cadastro de Funcionários")

with st.form("form_func"):
    nome = st.text_input("Nome")
    cargo = st.text_input("Cargo")
    ramal = st.text_input("Ramal")
    submit_func = st.form_submit_button("Cadastrar Funcionário")

    if submit_func:
        st.session_state.funcionarios.append({
            "nome": nome,
            "cargo": cargo,
            "ramal": ramal
        })
        st.success("Funcionário cadastrado!")

# ----------------------------
# AGENDAR REUNIÃO
# ----------------------------
st.header("📅 Agendar Reunião")

with st.form("form_reuniao"):
    data = st.date_input("Data", value=date.today())
    horario = st.text_input("Horário (ex: 09:00)")
    assunto = st.text_input("Assunto")

    sala_opcoes = [str(s["numero"]) for s in st.session_state.salas]
    funcionario_opcoes = [f["nome"] for f in st.session_state.funcionarios]

    sala = st.selectbox("Sala", sala_opcoes if sala_opcoes else ["Nenhuma"])
    funcionario = st.selectbox("Responsável", funcionario_opcoes if funcionario_opcoes else ["Nenhum"])

    submit_reuniao = st.form_submit_button("Agendar")

    if submit_reuniao:
        conflito = False

        for r in st.session_state.reunioes:
            if r["data"] == data and r["horario"] == horario and r["sala"] == sala:
                conflito = True

        if conflito:
            st.error("Conflito de horário nessa sala!")
        else:
            st.session_state.reunioes.append({
                "data": data,
                "horario": horario,
                "assunto": assunto,
                "sala": sala,
                "funcionario": funcionario
            })
            st.success("Reunião agendada!")

# ----------------------------
# LISTAR REUNIÕES
# ----------------------------
st.header("📋 Reuniões Agendadas")

for r in st.session_state.reunioes:
    st.write(f"📅 {r['data']} | ⏰ {r['horario']} | Sala {r['sala']} | {r['funcionario']} | {r['assunto']}")

# ----------------------------
# REALOCAR REUNIÃO
# ----------------------------
st.header("🔄 Realocar Reunião")

if st.session_state.reunioes:
    index = st.selectbox("Escolha a reunião", range(len(st.session_state.reunioes)))

    nova_data = st.date_input("Nova data", value=st.session_state.reunioes[index]["data"])
    novo_horario = st.text_input("Novo horário", st.session_state.reunioes[index]["horario"])
    nova_sala = st.selectbox("Nova sala", sala_opcoes)

    if st.button("Realocar"):
        st.session_state.reunioes[index]["data"] = nova_data
        st.session_state.reunioes[index]["horario"] = novo_horario
        st.session_state.reunioes[index]["sala"] = nova_sala
        st.success("Reunião realocada!")

# ----------------------------
# SALAS LIVRES
# ----------------------------
st.header("🔍 Verificar Salas Livres")

data_busca = st.date_input("Data para busca", value=date.today())
horario_busca = st.text_input("Horário (ex: 09:00)")

if st.button("Verificar"):
    ocupadas = []

    for r in st.session_state.reunioes:
        if r["data"] == data_busca and r["horario"] == horario_busca:
            ocupadas.append(r["sala"])

    livres = [s["numero"] for s in st.session_state.salas if str(s["numero"]) not in ocupadas]

    st.write("Salas livres:", livres)