import streamlit as st
import pandas as pd
from chatbot import chatbot_response
st.set_page_config(page_title="FS-Chatbot", layout="wide")
# FAQ laden
df = pd.read_csv("data/faq.csv")
# Session-State
if "messages" not in st.session_state:
    st.session_state.messages = []
# Chat-Bubble unten rechts
st.markdown("""
<style>
#chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background-color: #ff69b4;
    border-radius: 50%;
    text-align: center;
    line-height: 60px;
    font-weight: bold;
    color: white;
    cursor: pointer;
    z-index: 1000;
}
#chat-window {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 400px;
    height: 500px;
    background-color: white;
    border: 2px solid #ff69b4;
    border-radius: 10px;
    padding: 10px;
    overflow-y: auto;
    display: none;
    z-index: 999;
}
.user-msg { background-color:#ffe4e1; padding:5px 10px; border-radius:10px; margin-bottom:5px; text-align:right; }
.bot-msg { background-color:#ffb6c1; padding:5px 10px; border-radius:10px; margin-bottom:5px; text-align:left; }
</style>
<div id="chat-bubble">F S</div>
<div id="chat-window"></div>
<script>
const bubble = window.parent.document.getElementById('chat-bubble');
const chatWin = window.parent.document.getElementById('chat-window');
bubble.onclick = () => {
    chatWin.style.display = chatWin.style.display === "none" ? "block" : "none";
};
</script>
""", unsafe_allow_html=True)
# Chatfenster in Streamlit
st.subheader("Chatfenster")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)
user_input = st.text_input("Schreibe hier deine Nachricht:", key="input")
if st.button("Senden"):
    if user_input.strip() != "":
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = chatbot_response(user_input, df)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.experimental_rerun()
