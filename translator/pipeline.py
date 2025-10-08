import random
import re
import pandas as pd
import nltk
from nltk import pos_tag, word_tokenize


nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  # <— NEW LINE
nltk.download('averaged_perceptron_tagger', quiet=True)



# ---------- CLEANING ----------
def clean(t: str) -> str:
    """Cleans text by removing symbols, lowercasing, and normalizing whitespace."""
    t = t.lower()
    t = re.sub(r'[-]', ' ', t)
    t = re.sub(r'[^\w\s.,!?;:]', '', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'<U\\+0097>', ' ', t)
    return t.strip()


# ---------- LOAD DATA ----------
def load_data(path: str = "prez_data.xlsx") -> pd.DataFrame:
    """Loads and cleans presidential text dataset."""
    df = pd.read_excel(path)
    if 'clean' not in df.columns:
        df['clean'] = df['Text'].apply(clean)
 
    df['President'] = df['Name'].astype(str)
    return df


# ---------- BASIC REWRITER ----------
def rewrite(sentence: str, president: str, df: pd.DataFrame | None = None) -> str:
    """
    Basic presidential rewriter:
    Tokenizes user input and swaps random words with those from the president’s vocabulary.
    """
    if df is None:
        df = load_data()

    prez_df = df[df['President'].str.lower() == president.lower()]
    if prez_df.empty:
        return f"President '{president}' not found."

    # Tokenize both user sentence and president's text
    words = word_tokenize(clean(sentence))
    prez_text = " ".join(prez_df["clean"].astype(str).tolist())
    prez_tokens = word_tokenize(prez_text)
    prez_vocab = list(set(prez_tokens))

    # Replace words randomly
    out = []
    for w in words:
        if random.random() < 0.3:
            out.append(random.choice(prez_vocab))
        else:
            out.append(w)

    return " ".join(out).capitalize()


# ---------- ADVANCED (POS) REWRITER ----------
def rewrite_pos(sentence: str, president: str, df: pd.DataFrame | None = None) -> str:
    """
    POS-based rewriter: swaps words with the same part-of-speech (POS)
    from the selected president’s speeches.
    """
    if df is None:
        df = load_data()

    prez_df = df[df['President'].str.lower() == president.lower()]
    if prez_df.empty:
        return f"President '{president}' not found."

    prez_text = " ".join(prez_df["clean"].astype(str).tolist())
    prez_tokens = word_tokenize(prez_text)
    prez_pos = pos_tag(prez_tokens)

    # Build dict of president’s words grouped by POS
    prez_by_pos = {}
    for word, tag in prez_pos:
        prez_by_pos.setdefault(tag, []).append(word)

    # Tag the user’s input and replace by POS
    sent_tokens = word_tokenize(clean(sentence))
    sent_pos = pos_tag(sent_tokens)
    out = []

    for word, tag in sent_pos:
        if tag in prez_by_pos and random.random() < 0.5:
            out.append(random.choice(prez_by_pos[tag]))
        else:
            out.append(word)

    return " ".join(out).capitalize()
