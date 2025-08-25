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
# CSS für Bubble und Chat-Fenster
st.markdown("""
<style>
/* Bubble */
#fs-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background-color: #ff69b4;
    border-radius: 50%;
    color: white;
    font-weight: bold;
    font-size: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    z-index: 1000;
}
/* Chat-Fenster */
#fs-chat {
    position: fixed;
    bottom: 90px; /* direkt über der Bubble */
    right: 20px;
    width: 400px;
    height: 500px;
    background-color: white;
    border: 2px solid #ff69b4;
    border-radius: 10px;
    z-index: 999;
    padding: 10px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}
/* Nachrichtenbereich */
.fs-messages {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 10px;
}
/* Benutzertext */
.user-msg {
    background-color: #ffe4e1;
    padding: 5px 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    align-self: flex-end;
}
/* Bottext */
.bot-msg {
    background-color: #ffb6c1;
    padding: 5px 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    align-self: flex-start;
}
/* Eingabefeld */
#fs-input {
    width: 100%;
    padding: 5px;
}
</style>
""", unsafe_allow_html=True)
# Bubble anzeigen
st.markdown("<div id='fs-bubble'>F S</div>", unsafe_allow_html=True)
# Bubble-Click für Chatfenster
toggle = st.button(" ", key="bubble_toggle")
if toggle:
    st.session_state.chat_open = not st.session_state.chat_open
# Chat-Fenster
if st.session_state.chat_open:
    with st.container():
        st.markdown("<div id='fs-chat'>", unsafe_allow_html=True)
        st.markdown("<div class='fs-messages'>", unsafe_allow_html=True)
        # Alte Nachrichten anzeigen
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        # Neue Nachricht eingeben
        user_input = st.text_input("", key="fs_input_field")
        if user_input and st.button("Senden", key="send_button"):
            st.session_state.messages.append({"role": "user", "content": user_input})
            answer = chatbot_response(user_input, df)
            st.session_state.messages.append({"role": "assistant", "content": answer})
