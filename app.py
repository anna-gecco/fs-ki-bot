import streamlit as st
import pandas as pd
from chatbot import chatbot_response
# Seite konfigurieren
st.set_page_config(page_title="FS-KI-Chatbot", page_icon=":roboter:", layout="wide")
# FAQ laden
df = pd.read_csv("data/faq.csv")
# Session-State initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
# CSS für pinke Bubble
st.markdown("""
<style>
.stButton>button {
    background-color: #ff69b4;
    color: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
# Bubble als Button rechts unten
st.markdown("<div style='position: fixed; bottom: 20px; right: 20px;'>", unsafe_allow_html=True)
if st.button("F S"):
    st.session_state.chat_open = not st.session_state.chat_open
st.markdown("</div>", unsafe_allow_html=True)
# Chat-Fenster
if st.session_state.chat_open:
    st.markdown("<div style='position: fixed; bottom: 90px; right: 20px; width: 400px; height: 600px; background-color: white; border: 2px solid #ff69b4; border-radius: 10px; overflow-y: auto; padding:10px; z-index:9999;'>", unsafe_allow_html=True)
    # Alte Nachrichten anzeigen
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**Du:** {msg['content']}")
        else:
            st.markdown(f"**FS:** {msg['content']}")
    # Neue Nachricht eingeben
    user_input = st.text_input("Schreibe hier deine Frage:", key="input_field")
    if user_input and st.button("Senden"):
        # Nachricht speichern
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Antwort vom Chatbot
        answer = chatbot_response(user_input, df)
        st.session_state.messages.append({"role": "assistant", "content": answer})
