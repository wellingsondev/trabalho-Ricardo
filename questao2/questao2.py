import streamlit as st
from enum import Enum

# -----------------------------
# ENUMS (do diagrama)
# -----------------------------
class EnumCor(Enum):
    PRETO = "black"
    BRANCO = "white"
    AZUL = "blue"
    AMARELO = "yellow"
    CINZA = "gray"

class EnumTipo(Enum):
    EDIT = "input"
    MEMO = "textarea"
    LABEL = "label"

# -----------------------------
# CLASSE textoSaida
# -----------------------------
class TextoSaida:
    def __init__(self, texto="", tamanho=16, cor_fonte=EnumCor.PRETO, cor_fundo=EnumCor.BRANCO, tipo=EnumTipo.LABEL):
        self.texto = texto
        self.tamanho = tamanho
        self.cor_fonte = cor_fonte
        self.cor_fundo = cor_fundo
        self.tipo = tipo

    def criar_texto(self):
        estilo = f"""
        <div style="
            font-size:{self.tamanho}px;
            color:{self.cor_fonte.value};
            background-color:{self.cor_fundo.value};
            padding:10px;
            border-radius:8px;
        ">
            {self.texto}
        </div>
        """
        return estilo

    def mover_texto(self):
        return f"<marquee>{self.texto}</marquee>"

# -----------------------------
# INTERFACE
# -----------------------------
st.title("📝 Sistema Texto Saída")

# Criar objeto
texto_obj = TextoSaida()

# -----------------------------
# CONTROLES
# -----------------------------
st.sidebar.header("⚙️ Configurações")

# Tipo de componente
tipo = st.sidebar.selectbox(
    "Tipo de Texto",
    list(EnumTipo),
    format_func=lambda x: x.name
)

# Entrada de texto dinâmica
if tipo == EnumTipo.EDIT:
    texto = st.sidebar.text_input("Digite o texto")
elif tipo == EnumTipo.MEMO:
    texto = st.sidebar.text_area("Digite o texto")
else:
    texto = st.sidebar.text_input("Texto (Label)", value="Texto de exemplo")

# Tamanho
tamanho = st.sidebar.slider("Tamanho da fonte", 10, 60, 20)

# Cor fonte
cor_fonte = st.sidebar.selectbox(
    "Cor da Fonte",
    list(EnumCor),
    format_func=lambda x: x.name
)

# Cor fundo
cor_fundo = st.sidebar.selectbox(
    "Cor de Fundo",
    list(EnumCor),
    format_func=lambda x: x.name
)

# Atualizar objeto
texto_obj.texto = texto
texto_obj.tamanho = tamanho
texto_obj.cor_fonte = cor_fonte
texto_obj.cor_fundo = cor_fundo
texto_obj.tipo = tipo

# -----------------------------
# SAÍDA EM TEMPO REAL
# -----------------------------
st.subheader("📺 Visualização")

# Renderização HTML
st.markdown(texto_obj.criar_texto(), unsafe_allow_html=True)

# Botão mover texto
if st.button("🔄 Mover Texto"):
    st.markdown(texto_obj.mover_texto(), unsafe_allow_html=True)