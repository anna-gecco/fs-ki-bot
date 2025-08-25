import streamlit as st
import pandas as pd
from chatbot import chatbot_response  # Dein Chatbot-Modul
# Seite konfigurieren
st.set_page_config(page_title="FS-KI-Chatbot", page_icon=":roboter:", layout="wide")
# FAQ laden
df = pd.read_csv("data/faq.csv")  # Deine FAQ-Datei
# Session-State initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
# Platzhalter für Bubble und Chat
chat_placeholder = st.empty()
with chat_placeholder.container():
    # Bubble und Chat in Columns platzieren
    col1, col2, col3 = st.columns([6,1,1])  # Bubble rechts unten
    with col3:
        if st.button("F S"):
            st.session_state.chat_open = not st.session_state.chat_open
    # Chatfenster anzeigen, wenn Bubble geklickt
    if st.session_state.chat_open:
        chat_container = st.container()
        with chat_container:
            # Chatfenster Styling
            st.markdown("""
            <div style="
                width: 400px;
                height: 500px;
                background-color: white;
                border: 2px solid #ff69b4;
                border-radius: 10px;
                padding: 10px;
                display: flex;
                flex-direction: column;
                overflow-y: auto;
            ">
            """, unsafe_allow_html=True)
            # Nachrichtenbereich
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"<div style='background-color:#ffe4e1; padding:5px 10px; border-radius:10px; margin-bottom:5px; align-self:flex-end'>{msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background-color:#ffb6c1; padding:5px 10px; border-radius:10px; margin-bottom:5px; align-self:flex-start'>{msg['content']}</div>", unsafe_allow_html=True)
            # Eingabefeld + Senden-Button
            user_input = st.text_input("", key="chat_input")
            if st.button("Senden", key="send"):
                if user_input.strip() != "":
                    # Nachricht speichern
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    # Antwort vom Chatbot
                    answer = chatbot_response(user_input, df)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
