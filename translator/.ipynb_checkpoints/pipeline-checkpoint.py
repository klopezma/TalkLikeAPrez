import re
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean(t):
    t = t.lower()
    t = re.sub(r'[-]', ' ', t)
    t = re.sub(r'[^\w\s.,!?;:]', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'<U\\+0097>', ' ', t)
    return t.strip()

def translate_text(user_sentence: str, speeches_df: pd.DataFrame) -> str:
    user_sentence = user_sentence.lower()
    corpus = speeches_df['clean'].tolist() + [user_sentence]
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(corpus)
    sim = cosine_similarity(vectors[-1], vectors[:-1])
    idx = sim.argmax()
    similar_text = speeches_df.iloc[idx]['clean']
    sentences = re.split(r'[.!?]', similar_text)
    return random.choice(sentences).strip().capitalize()
