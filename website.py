import streamlit as st
import time
import g4f  # by xtekky

# Configura a página
st.set_page_config(page_title="🤖 ChatBot Multimodelo", page_icon="🤖", layout="wide")

# CSS moderno com efeito glassmorphism
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1F1C2C, #928DAB);
        font-family: 'Segoe UI', sans-serif;
        color: #ffffff;
    }
    h1 {
        text-align: center;
        margin-top: 30px;
        font-weight: 600;
    }
    .chat-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(12px);
        padding: 20px;
        max-width: 800px;
        margin: 30px auto;
        overflow-y: auto;
        height: 70vh;
    }
    .message {
        display: flex;
        align-items: flex-start;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 15px;
        max-width: 70%;
        animation: fadeInUp 0.3s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .message.user {
        background: linear-gradient(145deg, #1e88e5, #42a5f5);
        margin-left: auto;
        text-align: right;
        color: white;
    }
    .message.bot {
        background: rgba(255, 255, 255, 0.2);
        margin-right: auto;
        text-align: left;
    }
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        flex-shrink: 0;
    }
    .avatar.user {
        background: #1e88e5;
    }
    .avatar.bot {
        background: #ffffff33;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1>🤖 ChatBot Multimodelo</h1>", unsafe_allow_html=True)

# Lista de modelos
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

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 Selecione o Modelo")
    st.session_state.modelo = st.selectbox("Modelo", modelos_disponiveis, index=modelos_disponiveis.index(st.session_state.modelo))
    st.markdown("---")
    st.markdown("💡 Desenvolvido com Streamlit + g4f")

# Função para renderizar as mensagens
def render_chat():
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = f'<div class="avatar {role}"></div>'
        chat_html += f'<div class="message {role}">{avatar}<div>{msg["content"]}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

# Mostra o histórico do chat
render_chat()

# Input do usuário
user_input = st.text_input("Digite sua mensagem...", key="user_input", placeholder="Pergunte qualquer coisa...")

# Botão de enviar
send = st.button("Enviar")

# Quando o usuário envia uma mensagem
if user_input and send:
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_chat()
    time.sleep(0.5)

    try:
        resposta = g4f.ChatCompletion.create(
            model=st.session_state.modelo,
            provider=g4f.Provider.LegacyLMArena,
            messages=[{"role": "user", "content": user_input}]
        )
    except Exception as e:
        resposta = f"⚠️ Erro com o modelo **{st.session_state.modelo}**:\n\n```\n{str(e)}\n```"

    st.session_state.messages.append({"role": "bot", "content": resposta})

    # Limpa o input de texto com segurança
    st.session_state["user_input"] = ""

    # Atualiza a interface
    st.rerun()
