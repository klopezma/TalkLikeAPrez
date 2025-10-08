import random
import re
import pandas as pd
import nltk
from nltk import pos_tag, word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

def clean(t: str) -> str:
    t = t.lower()
    t = re.sub(r'[-]', ' ', t)
    t = re.sub(r'[^\w\s.,!?;:]', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'<U\\+0097>', ' ', t)
    return t.strip()

def fix_spacing(text: str) -> str:
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()

def load_data(path: str = "prez_data.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path)
    if 'clean' not in df.columns:
        df['clean'] = df['Text'].apply(clean)
    df['President'] = df['Name'].astype(str)
    return df

def rewrite(sentence: str, president: str, df: pd.DataFrame | None = None) -> str:
    if df is None:
        df = load_data()
    prez_df = df[df['President'].str.lower() == president.lower()]
    if prez_df.empty:
        return f"President '{president}' not found."
    words = word_tokenize(clean(sentence))
    prez_text = " ".join(prez_df["clean"].astype(str).tolist())
    prez_tokens = word_tokenize(prez_text)
    prez_vocab = list(set(prez_tokens))
    out = []
    for w in words:
        if random.random() < 0.3:
            out.append(random.choice(prez_vocab))
        else:
            out.append(w)
    return fix_spacing(" ".join(out).capitalize())

def rewrite_pos(sentence: str, president: str, df: pd.DataFrame | None = None) -> str:
    if df is None:
        df = load_data()
    prez_df = df[df['President'].str.lower() == president.lower()]
    if prez_df.empty:
        return f"President '{president}' not found."
    prez_text = " ".join(prez_df["clean"].astype(str).tolist())
    prez_tokens = word_tokenize(prez_text)
    prez_pos = pos_tag(prez_tokens)
    prez_by_pos = {}
    for word, tag in prez_pos:
        prez_by_pos.setdefault(tag, []).append(word)
    sent_tokens = word_tokenize(clean(sentence))
    sent_pos = pos_tag(sent_tokens)
    out = []
    for word, tag in sent_pos:
        if tag in prez_by_pos and random.random() < 0.5:
            out.append(random.choice(prez_by_pos[tag]))
        else:
            out.append(word)
    return fix_spacing(" ".join(out).capitalize())
