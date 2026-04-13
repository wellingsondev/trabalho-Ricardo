import streamlit as st

# -----------------------------
# CLASSES DO DIAGRAMA
# -----------------------------
class Musico:
    def __init__(self, nome):
        self.nome = nome

class Musica:
    def __init__(self, nome, duracao):
        self.nome = nome
        self.duracao = duracao

class Cd:
    def __init__(self, nome, coletanea, duplo):
        self.nome = nome
        self.coletanea = coletanea
        self.duplo = duplo
        self.musicos = []
        self.musicas = []

    def adicionar_musico(self, musico):
        self.musicos.append(musico)

    def adicionar_musica(self, musica):
        self.musicas.append(musica)

    def buscar_musica(self, nome):
        return [m for m in self.musicas if nome.lower() in m.nome.lower()]

# -----------------------------
# ESTADO GLOBAL
# -----------------------------
if "cds" not in st.session_state:
    st.session_state.cds = []

# -----------------------------
# INTERFACE
# -----------------------------
st.title("💿 Sistema de Coleção de CDs")

menu = st.sidebar.selectbox("Menu", [
    "Cadastrar CD",
    "Adicionar Músico",
    "Adicionar Música",
    "Listar CDs",
    "Buscar Música"
])

# -----------------------------
# CADASTRAR CD
# -----------------------------
if menu == "Cadastrar CD":
    st.subheader("➕ Novo CD")

    nome = st.text_input("Nome do CD")
    coletanea = st.checkbox("É coletânea?")
    duplo = st.checkbox("É duplo?")

    if st.button("Cadastrar CD"):
        cd = Cd(nome, coletanea, duplo)
        st.session_state.cds.append(cd)
        st.success("CD cadastrado!")

# -----------------------------
# ADICIONAR MÚSICO
# -----------------------------
elif menu == "Adicionar Músico":
    st.subheader("🎤 Adicionar Músico")

    if len(st.session_state.cds) == 0:
        st.warning("Cadastre um CD primeiro.")
    else:
        nomes_cd = [cd.nome for cd in st.session_state.cds]
        escolha = st.selectbox("Selecione o CD", nomes_cd)

        nome_musico = st.text_input("Nome do músico")

        if st.button("Adicionar"):
            cd = next(cd for cd in st.session_state.cds if cd.nome == escolha)
            cd.adicionar_musico(Musico(nome_musico))
            st.success("Músico adicionado!")

# -----------------------------
# ADICIONAR MÚSICA
# -----------------------------
elif menu == "Adicionar Música":
    st.subheader("🎵 Adicionar Música")

    if len(st.session_state.cds) == 0:
        st.warning("Cadastre um CD primeiro.")
    else:
        nomes_cd = [cd.nome for cd in st.session_state.cds]
        escolha = st.selectbox("Selecione o CD", nomes_cd)

        nome_musica = st.text_input("Nome da música")
        duracao = st.text_input("Duração (ex: 3:45)")

        if st.button("Adicionar"):
            cd = next(cd for cd in st.session_state.cds if cd.nome == escolha)
            cd.adicionar_musica(Musica(nome_musica, duracao))
            st.success("Música adicionada!")

# -----------------------------
# LISTAR CDs
# -----------------------------
elif menu == "Listar CDs":
    st.subheader("📋 Lista de CDs")

    if len(st.session_state.cds) == 0:
        st.warning("Nenhum CD cadastrado.")
    else:
        for cd in st.session_state.cds:
            st.markdown(f"### 💿 {cd.nome}")
            st.write(f"Coletânea: {'Sim' if cd.coletanea else 'Não'}")
            st.write(f"Duplo: {'Sim' if cd.duplo else 'Não'}")

            st.write("🎤 Músicos:")
            for m in cd.musicos:
                st.write(f"- {m.nome}")

            st.write("🎵 Músicas:")
            for mu in cd.musicas:
                st.write(f"- {mu.nome} ({mu.duracao})")

# -----------------------------
# BUSCAR MÚSICA
# -----------------------------
elif menu == "Buscar Música":
    st.subheader("🔍 Buscar Música")

    nome_busca = st.text_input("Digite o nome da música")

    if st.button("Buscar"):
        resultados = []

        for cd in st.session_state.cds:
            encontrados = cd.buscar_musica(nome_busca)
            for m in encontrados:
                resultados.append((cd.nome, m.nome, m.duracao))

        if resultados:
            for r in resultados:
                st.write(f"CD: {r[0]} | Música: {r[1]} | Duração: {r[2]}")
        else:
            st.warning("Nenhuma música encontrada.")