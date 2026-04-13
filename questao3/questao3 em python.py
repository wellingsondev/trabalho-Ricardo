import streamlit as st
from enum import Enum

# RNF04 - Código modular para futuras expansões [cite: 6]
class enuDirecao(Enum):
    CIMA = "cima"
    BAIXO = "baixo"
    ESQUERDA = "esquerda"
    DIREITA = "direita"

class Boneco:
    def __init__(self, nome: str, x: int = 0, y: int = 0, direcao: enuDirecao = enuDirecao.DIREITA):
        # RF01 e RNF02 - Atribuição de nome e coordenadas numéricas [cite: 1, 4]
        self.nome = nome
        self.posicaoX = x
        self.posicaoY = y
        self.direcao = direcao

    def moverBoneco(self, nova_direcao: enuDirecao):
        # RF04 - Validação de movimento compatível 
        # Exemplo de validação: impedir inversão imediata de 180 graus (opcional/lógica de negócio)
        opostos = {
            enuDirecao.CIMA: enuDirecao.BAIXO,
            enuDirecao.BAIXO: enuDirecao.CIMA,
            enuDirecao.ESQUERDA: enuDirecao.DIREITA,
            enuDirecao.DIREITA: enuDirecao.ESQUERDA
        }

        if nova_direcao == opostos.get(self.direcao):
            return False, f"Movimento inválido! O boneco não pode virar de {self.direcao.value} para {nova_direcao.value} diretamente."
        
        # RF02 e RF03 - Atualização de coordenadas e direção [cite: 2, 3]
        self.direcao = nova_direcao
        if nova_direcao == enuDirecao.CIMA: self.posicaoY += 1
        elif nova_direcao == enuDirecao.BAIXO: self.posicaoY -= 1
        elif nova_direcao == enuDirecao.ESQUERDA: self.posicaoX -= 1
        elif nova_direcao == enuDirecao.DIREITA: self.posicaoX += 1
        
        return True, "Movimento realizado com sucesso!"

# Configuração da Interface Streamlit
st.set_page_config(page_title="Boneco em Movimento", layout="centered")
st.title("🏃 Projeto: Boneco em Movimento")

# Inicialização do estado da sessão para persistir o objeto Boneco
if 'boneco' not in st.session_state:
    st.session_state.boneco = None

# Área de Criação (criarBoneco())
if st.session_state.boneco is None:
    with st.form("form_criacao"):
        nome_input = st.text_input("Nome do Boneco:", placeholder="Ex: Bob")
        submit = st.form_submit_button("Criar Boneco")
        if submit and nome_input:
            st.session_state.boneco = Boneco(nome_input)
            st.rerun()
else:
    boneco = st.session_state.boneco
    
    # Exibição de Status (RF02) [cite: 2]
    st.subheader(f"Status do {boneco.nome}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Posição X", boneco.posicaoX)
    col2.metric("Posição Y", boneco.posicaoY)
    col3.metric("Direção Atual", boneco.direcao.value.capitalize())

    # Controles de Movimento (RF03 e RNF03) [cite: 3, 5]
    st.divider()
    st.write("### Comandos de Movimento")
    
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("⬆️ Cima"):
        sucesso, msg = boneco.moverBoneco(enuDirecao.CIMA)
        if not sucesso: st.error(msg)
        else: st.rerun()

    if c2.button("⬇️ Baixo"):
        sucesso, msg = boneco.moverBoneco(enuDirecao.BAIXO)
        if not sucesso: st.error(msg)
        else: st.rerun()

    if c3.button("⬅️ Esquerda"):
        sucesso, msg = boneco.moverBoneco(enuDirecao.ESQUERDA)
        if not sucesso: st.error(msg)
        else: st.rerun()

    if c4.button("➡️ Direita"):
        sucesso, msg = boneco.moverBoneco(enuDirecao.DIREITA)
        if not sucesso: st.error(msg)
        else: st.rerun()

    if st.button("Reiniciar Sistema"):
        st.session_state.boneco = None
        st.rerun()