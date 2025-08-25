import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
def get_faq_answer(user_input, df):
    """Prüft, ob die Frage in den FAQ beantwortet werden kann"""
    vectorizer = TfidfVectorizer()
    faq_vectors = vectorizer.fit_transform(df["frage"])
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, faq_vectors)
    idx = similarity.argmax()
    score = similarity[0, idx]
    if score > 0.5:
        return df.iloc[idx]["antwort"]
    return None
def get_ai_answer(user_input):
    """Fragt die KI über die neue OpenAI API"""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=300
    )
    return response.choices[0].message.content
def chatbot_response(user_input, faq_df):
    """Erst FAQ prüfen, dann KI"""
    faq_answer = get_faq_answer(user_input, faq_df)
    if faq_answer:
        return faq_answer
    else:
        return get_ai_answer(user_input)