import streamlit as st
import pandas as pd
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
st.markdown(
    "Stelle deine Fragen! Der Chatbot prüft zuerst unsere FAQs, "
    "wenn nichts gefunden wird, nutzt er die KI."
)
# -----------------------------
# Session-State für Chatverlauf & FAQs
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv("data/faq.csv")
# -----------------------------
# Upload-Funktion für neue FAQs
# -----------------------------
uploaded_file = st.file_uploader(
    "Lade hier eine CSV mit neuen Fragen/Antworten hoch (frage,antwort)",
    type="csv"
)
if uploaded_file:
    try:
        new_df = pd.read_csv(uploaded_file)
        # Überprüfen, ob Spalten existieren
        if "frage" in new_df.columns and "antwort" in new_df.columns:
            st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
            st.success("Datei erfolgreich hinzugefügt! Chatbot kann jetzt neue Fragen beantworten.")
        else:
            st.error("Die CSV muss genau die Spalten 'frage' und 'antwort' enthalten.")
    except Exception as e:
        st.error(f"Fehler beim Hochladen: {e}")
# -----------------------------
# Chat-Nachrichten anzeigen
# -----------------------------
for msg in st.session_state.messages:
    role = msg["role"]
    st.chat_message(role).markdown(msg["content"])
# -----------------------------
# Neue Nutzer-Eingabe
# -----------------------------
user_input = st.chat_input("Schreib deine Frage hier...")
if user_input:
    # User-Nachricht speichern und anzeigen
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    # Antwort vom Chatbot
    # Wir übergeben die aktuelle FAQ-Datenbank
    try:
        answer = chatbot_response(user_input, faq_df=st.session_state.df)
    except Exception as e:
        answer = f"Fehler bei der Antwort: {e}"
    # Antwort speichern und anzeigen
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").markdown(answer)