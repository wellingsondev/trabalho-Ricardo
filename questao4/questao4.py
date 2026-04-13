import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- CLASSES DO SISTEMA (Baseadas no Diagrama de Classes) ---

class Paciente:
    def __init__(self, nome, cpf, data_nasc, historico=""):
        self.nome = nome
        self.cpf = cpf
        self.dataNascimento = data_nasc
        self.historico = historico

class Medico:
    def __init__(self, nome, rgm, idade, especialidade):
        self.nome = nome
        self.rgm = rgm
        self.idade = idade
        self.especialidade = especialidade

class Remedio:
    def __init__(self, nome, vencimento, quantidade):
        self.nome = nome
        self.vencimento = vencimento
        self.quantidade = quantidade

class Atendimento:
    def __init__(self, paciente, medico, data, horario, diagnostico):
        self.paciente = paciente
        self.medico = medico
        self.data = data
        self.horario = horario
        self.diagnostico = diagnostico
        self.lista_remedios = []

    def adicionar_remedio(self, remedio):
        self.lista_remedios.append(remedio)

# --- CONFIGURAÇÃO DA INTERFACE (RNF002: Tempo de resposta rápido) ---

st.set_page_config(page_title="Policlínica - Prontuário Eletrônico", layout="wide")

# Inicialização do Banco de Dados em Memória (Session State)
if 'pacientes' not in st.session_state: st.session_state.pacientes = []
if 'medicos' not in st.session_state: st.session_state.medicos = []
if 'remedios' not in st.session_state: st.session_state.remedios = []
if 'atendimentos' not in st.session_state: st.session_state.atendimentos = []

st.title("🏥 Sistema de Prontuário Eletrônico")

menu = st.sidebar.selectbox("Navegação", 
    ["Início", "Gerenciar Pacientes", "Gerenciar Médicos", "Gerenciar Remédios", "Realizar Atendimento", "Planilhas"])

# --- FUNCIONALIDADES ---

# RF001 - Gerenciar Paciente
if menu == "Gerenciar Pacientes":
    st.header("👥 Gerenciamento de Pacientes")
    with st.form("cadastro_paciente"):
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        data_nasc = st.date_input("Data de Nascimento", min_value=date(1900, 1, 1))
        historico = st.text_area("Histórico Médico")
        if st.form_submit_button("Cadastrar Paciente"):
            st.session_state.pacientes.append(Paciente(nome, cpf, data_nasc, historico))
            st.success(f"Paciente {nome} cadastrado com sucesso!")

    if st.session_state.pacientes:
        st.write("### Pacientes Cadastrados")
        st.table(pd.DataFrame([vars(p) for p in st.session_state.pacientes]))

# RF002 - Gerenciar Médico
elif menu == "Gerenciar Médicos":
    st.header("👨‍⚕️ Gerenciamento de Médicos")
    with st.form("cadastro_medico"):
        nome = st.text_input("Nome do Médico")
        rgm = st.text_input("RGM")
        idade = st.number_input("Idade", min_value=20, max_value=100)
        especialidade = st.text_input("Especialidade")
        if st.form_submit_button("Cadastrar Médico"):
            st.session_state.medicos.append(Medico(nome, rgm, idade, especialidade))
            st.success(f"Médico {nome} cadastrado!")

    if st.session_state.medicos:
        st.write("### Corpo Clínico")
        st.table(pd.DataFrame([vars(m) for m in st.session_state.medicos]))

# RF003 - Gerenciar Remédio
elif menu == "Gerenciar Remédios":
    st.header("💊 Estoque de Remédios")
    with st.form("cadastro_remedio"):
        nome = st.text_input("Nome do Medicamento")
        vencimento = st.date_input("Data de Vencimento")
        quantidade = st.number_input("Quantidade em Estoque", min_value=0)
        if st.form_submit_button("Adicionar Remédio"):
            st.session_state.remedios.append(Remedio(nome, vencimento, quantidade))
            st.success(f"Remédio {nome} adicionado!")

    if st.session_state.remedios:
        st.table(pd.DataFrame([vars(r) for r in st.session_state.remedios]))

# RF005 - Realizar Atendimento Clínica
elif menu == "Realizar Atendimento":
    st.header("🩺 Novo Atendimento")
    if not st.session_state.pacientes or not st.session_state.medicos:
        st.warning("É necessário cadastrar ao menos um paciente e um médico antes.")
    else:
        with st.form("atendimento_form"):
            paciente_nome = st.selectbox("Selecionar Paciente", [p.nome for p in st.session_state.pacientes])
            medico_nome = st.selectbox("Selecionar Médico", [m.nome for m in st.session_state.medicos])
            data_atend = st.date_input("Data", value=datetime.now())
            horario = st.time_input("Horário")
            diagnostico = st.text_area("Diagnóstico Clínica")
            
            remedios_selecionados = st.multiselect("Prescrever Remédios (RF004)", [r.nome for r in st.session_state.remedios])
            
            if st.form_submit_button("Finalizar Atendimento"):
                p_obj = next(p for p in st.session_state.pacientes if p.nome == paciente_nome)
                m_obj = next(m for m in st.session_state.medicos if m.nome == medico_nome)
                
                novo_atend = Atendimento(p_obj.nome, m_obj.nome, data_atend, horario, diagnostico)
                novo_atend.lista_remedios = remedios_selecionados
                st.session_state.atendimentos.append(novo_atend)
                st.success("Atendimento registrado com sucesso!")

# RF004 - Gerar planilha de horário de remédio
elif menu == "Planilhas":
    st.header("📊 Relatórios e Planilhas")
    if st.session_state.atendimentos:
        st.write("### Histórico de Atendimentos e Prescrições")
        dados_planilha = []
        for a in st.session_state.atendimentos:
            dados_planilha.append({
                "Paciente": a.paciente,
                "Médico": a.medico,
                "Data": a.data,
                "Remédios Prescritos": ", ".join(a.lista_remedios),
                "Diagnóstico": a.diagnostico
            })
        df = pd.DataFrame(dados_planilha)
        st.dataframe(df)
        
        # Simulação de exportação (RNF001 - Integridade dos dados)
        st.download_button("Baixar Planilha de Atendimentos (CSV)", df.to_csv(index=False), "planilha_policlinica.csv")
    else:
        st.info("Nenhum atendimento realizado até o momento.")

else:
    st.write("Selecione uma opção no menu lateral para começar.")
    st.info("Sistema operando sob protocolo de segurança RNF001.")