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
  body { font-family: Arial, sans-serif; margin:0; }
  /* Pinke Bubble */
  #chat-bubble {
    position: fixed; right: 20px; bottom: 20px; width: 62px; height: 62px;
    border-radius: 50%; background: #ff4da6; color:#fff; display:flex;
    align-items:center; justify-content:center; font-weight:700; cursor:pointer;
    box-shadow:0 10px 30px rgba(255,77,166,.35); z-index: 9999; user-select:none;
  }
  /* Fenster */
  #chatbox {
    position: fixed; right: 20px; bottom: 92px; width: 360px; max-height: 70vh;
    display:none; flex-direction:column; background:#fff; border-radius:14px;
    box-shadow:0 18px 60px rgba(0,0,0,.18); overflow:hidden; z-index: 9999;
  }
  .header { background:#ff4da6; color:#fff; padding:12px 14px; font-weight:700; display:flex; justify-content:space-between; }
  .messages { padding:12px; overflow:auto; flex:1; background:#fff6fb; }
  .msg { margin: 8px 0; }
  .bubble { display:inline-block; padding:8px 12px; border-radius:12px; max-width:80%; line-height:1.35; }
  .bot   .bubble { background:#ffe1ef; color:#000; }
  .user  .bubble { background:#ff4da6; color:#fff; float:right; }
  .input { display:flex; border-top:1px solid #f0c6d9; }
  #userInput { flex:1; padding:10px; border:0; outline:none; }
  #sendBtn  { border:0; background:#ff4da6; color:#fff; padding:0 14px; cursor:pointer; }
  .meta { font-size:12px; color:#7a4660; padding:6px 12px; background:#fff; border-top:1px dashed #f3c7dc; }
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
