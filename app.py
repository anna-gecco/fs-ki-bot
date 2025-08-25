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
# Bubble + Chat-Fenster alles in Streamlit
st.markdown(
    """
    <style>
    .bubble {
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
    .chat-box {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 400px;
        height: 500px;
        background-color: white;
        border: 2px solid #ff69b4;
        border-radius: 10px;
        z-index: 999;
        display: flex;
        flex-direction: column;
        padding: 10px;
        overflow: hidden;
    }
    .messages {
        flex: 1;
        overflow-y: auto;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #ffe4e1;
        padding: 5px 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        align-self: flex-end;
    }
    .bot-msg {
        background-color: #ffb6c1;
        padding: 5px 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        align-self: flex-start;
    }
    </style>
    """, unsafe_allow_html=True
)
# Bubble als Streamlit-Button simulieren
bubble_col1, bubble_col2, bubble_col3 = st.columns([1,1,6])
with bubble_col3:
    if st.button("F S", key="bubble"):
        st.session_state.chat_open = not st.session_state.chat_open
# Chat-Fenster
if st.session_state.chat_open:
    with st.container():
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        # Nachrichtenbereich
        st.markdown('<div class="messages">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Eingabefeld + Senden-Button
        user_input = st.text_input("Schreibe hier deine Frage:", key="chat_input")
        if st.button("Senden", key="send"):
            if user_input.strip() != "":
                st.session_state.messages.append({"role": "user", "content": user_input})
                answer = chatbot_response(user_input, df)
                st.session_state.messages.append({"role": "assistant", "content": answer})
