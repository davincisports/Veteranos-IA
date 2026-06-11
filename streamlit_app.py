import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="IA do Clube", page_icon="⚽")

# Configurar a chave da API (Vem das Secrets)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("A chave da API não foi encontrada nas Secrets. Verifica as configurações.")

# --- PERSONALIDADE DA IA ---
SYSTEM_INSTRUCTION = """
Tu és a 'Dra. Sofia', a secretária virtual do Clube GDCFF Veteranos.
És simpática, organizada e profissional.
O teu trabalho é ajudar sócios e jogadores com informações sobre jogos, quotas e eventos.
Se não souberes algo, diz que vais consultar a direção.
Usa emojis para ser mais amigável.
"""

# Inicializar o modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- INTERFACE ---
st.title("⚽ GDCFF Assistente Virtual")
st.write("Olá! Sou a IA do teu clube. Pergunta-me sobre jogos ou quotas.")

# Gestão do histórico de chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Input do utilizador
user_input = st.chat_input("Escreve aqui a tua dúvida...")

if user_input:
    # Mostrar pergunta
    st.chat_message("user").markdown(user_input)
    
    # Obter resposta
    try:
        response = st.session_state.chat.send_message(user_input)
        st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
