import streamlit as st
from datetime import date

# -----------------------------
# CLASSES
# -----------------------------
class Endereco:
    def __init__(self, cod, logradouro, bairro):
        self.cod = cod
        self.logradouro = logradouro
        self.bairro = bairro

class Telefone:
    def __init__(self, ddd, ddi, numero):
        self.ddd = ddd
        self.ddi = ddi
        self.numero = numero

class Pessoa:
    def __init__(self, nome, data_nasc):
        self.nome = nome
        self.data_nasc = data_nasc
        self.enderecos = []
        self.telefones = []

    def adicionar_endereco(self, endereco):
        self.enderecos.append(endereco)

    def adicionar_telefone(self, telefone):
        self.telefones.append(telefone)

class Profissao:
    def __init__(self, idProf, nome):
        self.idProf = idProf
        self.nome = nome

class Cargo:
    def __init__(self, idCargo, descricao):
        self.idCargo = idCargo
        self.descricao = descricao

class Cliente(Pessoa):
    def __init__(self, nome, data_nasc, cod, limite, dtCompra):
        super().__init__(nome, data_nasc)
        self.cod = cod
        self.limite = limite
        self.dtCompra = dtCompra
        self.profissao = None

class Funcionario(Pessoa):
    def __init__(self, nome, data_nasc, matricula, salario, dtAdmissao):
        super().__init__(nome, data_nasc)
        self.matricula = matricula
        self.salario = salario
        self.dtAdmissao = dtAdmissao
        self.cargo = None

# -----------------------------
# ESTADO
# -----------------------------
if "pessoas" not in st.session_state:
    st.session_state.pessoas = []

if "clientes" not in st.session_state:
    st.session_state.clientes = []

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = []

# -----------------------------
# INTERFACE
# -----------------------------
st.title("👥 Sistema de Pessoas, Clientes e Funcionários")

menu = st.sidebar.selectbox("Menu", [
    "Cadastrar Pessoa",
    "Adicionar Endereço",
    "Adicionar Telefone",
    "Cadastrar Cliente",
    "Cadastrar Funcionário",
    "Associar Profissão",
    "Associar Cargo",
    "Listar Dados"
])

# -----------------------------
# CADASTRAR PESSOA
# -----------------------------
if menu == "Cadastrar Pessoa":
    st.subheader("➕ Pessoa")

    nome = st.text_input("Nome")
    data = st.date_input("Data de Nascimento")

    if st.button("Cadastrar"):
        st.session_state.pessoas.append(Pessoa(nome, data))
        st.success("Pessoa cadastrada!")

# -----------------------------
# ADICIONAR ENDEREÇO
# -----------------------------
elif menu == "Adicionar Endereço":
    st.subheader("🏠 Endereço")

    if not st.session_state.pessoas:
        st.warning("Cadastre uma pessoa primeiro.")
    else:
        nomes = [p.nome for p in st.session_state.pessoas]
        escolha = st.selectbox("Pessoa", nomes)

        cod = st.number_input("Código", 0)
        logradouro = st.text_input("Logradouro")
        bairro = st.text_input("Bairro")

        if st.button("Adicionar"):
            pessoa = next(p for p in st.session_state.pessoas if p.nome == escolha)
            pessoa.adicionar_endereco(Endereco(cod, logradouro, bairro))
            st.success("Endereço adicionado!")

# -----------------------------
# ADICIONAR TELEFONE
# -----------------------------
elif menu == "Adicionar Telefone":
    st.subheader("📞 Telefone")

    if not st.session_state.pessoas:
        st.warning("Cadastre uma pessoa primeiro.")
    else:
        nomes = [p.nome for p in st.session_state.pessoas]
        escolha = st.selectbox("Pessoa", nomes)

        ddd = st.text_input("DDD")
        ddi = st.text_input("DDI")
        numero = st.text_input("Número")

        if st.button("Adicionar"):
            pessoa = next(p for p in st.session_state.pessoas if p.nome == escolha)
            pessoa.adicionar_telefone(Telefone(ddd, ddi, numero))
            st.success("Telefone adicionado!")

# -----------------------------
# CADASTRAR CLIENTE
# -----------------------------
elif menu == "Cadastrar Cliente":
    st.subheader("🧾 Cliente")

    if not st.session_state.pessoas:
        st.warning("Cadastre uma pessoa primeiro.")
    else:
        nomes = [p.nome for p in st.session_state.pessoas]
        escolha = st.selectbox("Pessoa", nomes)

        cod = st.number_input("Código", 0)
        limite = st.number_input("Limite", 0.0)
        dtCompra = st.date_input("Data Compra")

        if st.button("Cadastrar Cliente"):
            pessoa = next(p for p in st.session_state.pessoas if p.nome == escolha)
            cliente = Cliente(pessoa.nome, pessoa.data_nasc, cod, limite, dtCompra)
            cliente.enderecos = pessoa.enderecos
            cliente.telefones = pessoa.telefones
            st.session_state.clientes.append(cliente)
            st.success("Cliente cadastrado!")

# -----------------------------
# CADASTRAR FUNCIONÁRIO
# -----------------------------
elif menu == "Cadastrar Funcionário":
    st.subheader("💼 Funcionário")

    if not st.session_state.pessoas:
        st.warning("Cadastre uma pessoa primeiro.")
    else:
        nomes = [p.nome for p in st.session_state.pessoas]
        escolha = st.selectbox("Pessoa", nomes)

        matricula = st.number_input("Matrícula", 0)
        salario = st.number_input("Salário", 0.0)
        dtAdm = st.date_input("Data Admissão")

        if st.button("Cadastrar Funcionário"):
            pessoa = next(p for p in st.session_state.pessoas if p.nome == escolha)
            func = Funcionario(pessoa.nome, pessoa.data_nasc, matricula, salario, dtAdm)
            func.enderecos = pessoa.enderecos
            func.telefones = pessoa.telefones
            st.session_state.funcionarios.append(func)
            st.success("Funcionário cadastrado!")

# -----------------------------
# ASSOCIAR PROFISSÃO
# -----------------------------
elif menu == "Associar Profissão":
    st.subheader("🎓 Profissão")

    if not st.session_state.clientes:
        st.warning("Cadastre um cliente primeiro.")
    else:
        nomes = [c.nome for c in st.session_state.clientes]
        escolha = st.selectbox("Cliente", nomes)

        idProf = st.number_input("ID Profissão", 0)
        nomeProf = st.text_input("Nome Profissão")

        if st.button("Associar"):
            cliente = next(c for c in st.session_state.clientes if c.nome == escolha)
            cliente.profissao = Profissao(idProf, nomeProf)
            st.success("Profissão associada!")

# -----------------------------
# ASSOCIAR CARGO
# -----------------------------
elif menu == "Associar Cargo":
    st.subheader("🏢 Cargo")

    if not st.session_state.funcionarios:
        st.warning("Cadastre um funcionário primeiro.")
    else:
        nomes = [f.nome for f in st.session_state.funcionarios]
        escolha = st.selectbox("Funcionário", nomes)

        idCargo = st.number_input("ID Cargo", 0)
        desc = st.text_input("Descrição")

        if st.button("Associar"):
            func = next(f for f in st.session_state.funcionarios if f.nome == escolha)
            func.cargo = Cargo(idCargo, desc)
            st.success("Cargo associado!")

# -----------------------------
# LISTAR DADOS
# -----------------------------
elif menu == "Listar Dados":
    st.subheader("📋 Dados")

    st.write("### 👤 Pessoas")
    for p in st.session_state.pessoas:
        st.write(f"{p.nome} - {p.data_nasc}")
        for e in p.enderecos:
            st.write(f"  🏠 {e.logradouro}, {e.bairro}")
        for t in p.telefones:
            st.write(f"  📞 {t.ddd}-{t.numero}")

    st.write("### 🧾 Clientes")
    for c in st.session_state.clientes:
        st.write(f"{c.nome} | Limite: {c.limite}")
        if c.profissao:
            st.write(f"  🎓 {c.profissao.nome}")

    st.write("### 💼 Funcionários")
    for f in st.session_state.funcionarios:
        st.write(f"{f.nome} | Salário: {f.salario}")
        if f.cargo:
            st.write(f"  🏢 {f.cargo.descricao}")