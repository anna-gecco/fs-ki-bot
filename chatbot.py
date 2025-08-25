import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
# :schlüssel: OpenAI API-Key aus Umgebungsvariable
openai.api_key = os.getenv("OPENAI_API_KEY")
# -----------------------------
# FAQ-Daten laden
# -----------------------------
df = pd.read_csv("data/faq.csv")
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(df["frage"])
# -----------------------------
# Funktionen
# -----------------------------
def get_faq_answer(user_input):
    """
    Prüft, ob die Frage in den FAQ beantwortet werden kann.
    Gibt die Antwort zurück, falls Ähnlichkeit hoch genug.
    """
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, faq_vectors)
    idx = similarity.argmax()
    score = similarity[0, idx]
    if score > 0.5:  # Schwellenwert für Treffer
        return df.iloc[idx]["antwort"]
    return None
def get_ai_answer(user_input):
    """
    Fragt die KI (günstiges Modell gpt-4o-mini) über die neue OpenAI API
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=300
    )
    return response.choices[0].message.content
def chatbot_response(user_input):
    """
    Hauptfunktion: Erst FAQ prüfen, dann KI
    """
    faq_answer = get_faq_answer(user_input)
    if faq_answer:
        return faq_answer
    else:
        return get_ai_answer(user_input)
