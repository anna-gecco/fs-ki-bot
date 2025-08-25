import streamlit as st
from chatbot import chatbot_response
# -----------------------------
# Streamlit-Seite konfigurieren
# -----------------------------
st.set_page_config(
    page_title="FS-KI-Chatbot",
    page_icon=":roboter:",
    layout="centered"
)
st.title(":roboter: FS-KI-Chatbot")
st.markdown("Stelle mir deine Fragen! Zuerst wird geprüft, ob deine Frage in unseren FAQs beantwortet werden kann. Wenn nicht, greife ich auf die KI zurück.")
# -----------------------------
# Session-State für Chatverlauf
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
# Chat-Nachrichten anzeigen
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
# -----------------------------
# Neue Nutzer-Eingabe
# -----------------------------
user_input = st.chat_input("Schreib deine Frage hier...")
if user_input:
    # User-Nachricht speichern und anzeigen
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    # Antwort vom Chatbot (FAQ zuerst, dann KI)
    answer = chatbot_response(user_input)
    # Antwort speichern und anzeigen
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").markdown(answer)
