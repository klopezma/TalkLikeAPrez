import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from translator.pipeline import rewrite, rewrite_pos, load_data


# Load data (if needed)
df = pd.read_excel("prez_data.xlsx")
presidents = sorted(df['Name'].unique())

# --- Streamlit UI ---
st.title("🇺🇸 Talk Like a President")
st.write("Enter a sentence and see how it sounds when rewritten in a presidential tone!")

# Dropdown for president
prezPick = st.selectbox("🎩 Choose a President", presidents)

# Text input for sentence
sentence = st.text_area("💬 Enter what you'd like to rewrite:")

# Button
if st.button("Translate"):
    if sentence.strip():
        # Run both translators
        basic_output = rewrite(sentence, prezPick)
        pos_output = rewrite_pos(sentence, prezPick)

        # Display side by side
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🧱 Basic Rewriter")
            st.success(basic_output)
        with col2:
            st.subheader("🧠 POS-Based Rewriter")
            st.info(pos_output)
    else:
        st.warning("Please enter a sentence to translate.")
