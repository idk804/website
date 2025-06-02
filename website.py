import streamlit as st
import time
import g4f  # Biblioteca g4f do xtekky

# Configuração da página
st.set_page_config(page_title="🤖 ChatBot Multimodelo", page_icon="🤖", layout="wide")

# Estilo com efeito moderno
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}
h1 {
    text-align: center;
    color: #ffffff;
    margin-top: 30px;
}
.chat-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    max-width: 900px;
    margin: auto;
    height: 70vh;
    overflow-y: auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.message {
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 12px;
    max-width: 75%;
    animation: fadeIn 0.3s ease-out;
}
.message.user {
    background: #2196f3;
    margin-left: auto;
    color: white;
}
.message.bot {
    background: rgba(255, 255, 255, 0.15);
    margin-right: auto;
    color: white;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1>🤖 ChatBot Multimodelo</h1>", unsafe_allow_html=True)

# Lista de modelos suportados
modelos_disponiveis = [
    "gpt-4o",
    "gpt-4",
    "o3",
    "o4-mini",
    "claude-3.7-sonnet",
    "claude-3.7-sonnet-thinking",
    "grok-3"
]

# Estado inicial
if "messages" not in st.session_state:
    st.session_state.messages = []

if "modelo" not in st.session_state:
    st.session_state.modelo = "gpt-4o"

# ✅ Reset de campo de input com método moderno
if "reset" in st.query_params:
    st.session_state["user_input"] = ""
    st.query_params.clear()

# Sidebar
with st.sidebar:
    st.markdown("### 🔍 Escolha o Modelo")
    st.session_state.modelo = st.selectbox("Modelo", modelos_disponiveis, index=modelos_disponiveis.index(st.session_state.modelo))
    st.markdown("ℹ️ Usando `LegacyLMArena` do g4f")
    st.markdown("---")
    if st.button("🧹 Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# Função para exibir o chat
def render_chat():
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "bot"
        chat_html += f'<div class="message {role_class}">{msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

# Exibir histórico do chat
render_chat()

# Campo de entrada
user_input = st.text_input("Digite sua pergunta:", key="user_input", placeholder="Fale com o chatbot...")

# Botão para enviar
send = st.button("Enviar")

if user_input and send:
    # Armazena mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_chat()
    time.sleep(0.4)

    # Gera resposta com g4f
    try:
        resposta = g4f.ChatCompletion.create(
            model=st.session_state.modelo,
            provider=g4f.Provider.LegacyLMArena,
            messages=[{"role": "user", "content": user_input}]
        )
    except Exception as e:
        resposta = f"❌ Erro: {str(e)}"

    # Armazena resposta do bot
    st.session_state.messages.append({"role": "bot", "content": resposta})

    # Força a limpeza do input (sem erro de SessionState)
    st.query_params["reset"] = "1"
    st.rerun()
