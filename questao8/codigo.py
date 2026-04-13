import streamlit as st

# --- DEFINIÇÃO DAS CLASSES (Baseado no Diagrama de Classe) ---

class Cd:
    """Representa um CD individual na coleção."""
    def __init__(self, titulo: str, artista: str, ano_lancamento: int):
        # RF01, RF02 e RF03: Registro de artista, título e ano 
        self.titulo = titulo
        self.artista = artista
        self.anoLancamento = ano_lancamento

    def exibirDados(self):
        """Formata os dados do CD para exibição rápida."""
        return f"**{self.titulo}** - {self.artista} ({self.anoLancamento})"

class Colecao:
    """Gerencia a lista de CDs cadastrados."""
    def __init__(self):
        # Atributo derivado: listaCds [1..*] conforme diagrama
        self.listaCds = []

    def adicionarCd(self, cd: Cd):
        """Adiciona um objeto Cd à coleção."""
        self.listaCds.append(cd)

    def pesquisarCd(self, termo: str):
        """Filtra CDs por título ou artista para consulta rápida."""
        return [cd for cd in self.listaCds if termo.lower() in cd.titulo.lower() or termo.lower() in cd.artista.lower()]

# --- INTERFACE STREAMLIT (RNF01 e RNF02: Leve e rápida) ---

st.set_page_config(page_title="Coleção de CDs do Adriano", layout="centered")

# Inicialização do estado da sessão para persistência dos dados
if 'colecao' not in st.session_state:
    st.session_state.colecao = Colecao()

colecao = st.session_state.colecao

st.title("📀 Inventário de CDs")
st.write("Gerencie sua coleção de forma rápida e simples.")

# Área de Cadastro (RF01, RF02, RF03)
# RNF02: Prioriza entrada de texto rápida 
with st.expander("➕ Cadastrar Novo CD", expanded=True):
    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        titulo_input = col1.text_input("Título do CD")
        artista_input = col1.text_input("Artista (Cantor/Banda)")
        ano_input = col2.number_input("Ano", min_value=1900, max_value=2100, value=2024)
        
        btn_cadastrar = st.form_submit_button("Adicionar à Coleção")
        
        if btn_cadastrar:
            if titulo_input and artista_input:
                novo_cd = Cd(titulo_input, artista_input, int(ano_input))
                colecao.adicionarCd(novo_cd)
                st.success(f"'{titulo_input}' adicionado com sucesso!")
            else:
                st.error("Por favor, preencha o título e o artista.")

# Área de Consulta (RF04: Listagem para consulta) 
st.divider()
st.subheader("🔍 Sua Coleção")

busca = st.text_input("Pesquisar por título ou artista...")

cds_para_exibir = colecao.pesquisarCd(busca) if busca else colecao.listaCds

if not cds_para_exibir:
    st.info("Nenhum CD encontrado na coleção.")
else:
    # Exibe a lista formatada (RNF01: Interface leve) 
    for i, cd in enumerate(cds_para_exibir):
        st.write(f"{i+1}. {cd.exibirDados()}")