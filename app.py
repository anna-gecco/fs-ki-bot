import streamlit as st
import pandas as pd
from chatbot import chatbot_response
# -----------------------------
# Seite konfigurieren
# -----------------------------
st.set_page_config(
    page_title="FS-KI-Chatbot",
    page_icon=":roboter:",
    layout="wide"
)
# -----------------------------
# CSS für pinke Bubble
# -----------------------------
st.markdown("""
<style>
#fs-chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background-color: #ff69b4;
    border-radius: 50%;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    cursor: pointer;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    font-size: 24px;
}
#fs-chat-window {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 400px;
    height: 600px;
    display: none;
    z-index: 9999;
    border: 2px solid #ff69b4;
    border-radius: 10px;
    background-color: white;
    padding: 10px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)
# -----------------------------
# FAQ-Daten laden
# -----------------------------
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv("data/faq.csv")
# -----------------------------
# Session-State für Bubble & Chat
# -----------------------------
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []
# -----------------------------
# Bubble anzeigen
# -----------------------------
bubble_html = '<div id="fs-chat-bubble">F S</div>'
st.markdown(bubble_html, unsafe_allow_html=True)
# -----------------------------
# JS für Klick-Event auf Bubble
# -----------------------------
st.markdown("""
<script>
const bubble = window.parent.document.getElementById('fs-chat-bubble');
bubble.onclick = () => {
    const chat = document.getElementById('fs-chat-window');
    if(chat.style.display === 'none'){
        chat.style.display = 'block';
    } else {
        chat.style.display = 'none';
    }
};
</script>
""", unsafe_allow_html=True)
# -----------------------------
# Chat-Fenster direkt in Streamlit
# -----------------------------
chat_container = st.container()
with chat_container:
    if st.session_state.chat_open:
        st.markdown('<div id="fs-chat-window">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**Du:** {msg['content']}")
            else:
                st.markdown(f"**FS:** {msg['content']}")
        st.markdown('</div>', unsafe_allow_html=True)
        user_input = st.text_input("Schreibe hier deine Frage:")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            answer = chatbot_response(user_input, st.session_state.df)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.experimental_rerun()
