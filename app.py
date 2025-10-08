import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from translator.pipeline import rewrite, rewrite_pos, load_data


# Load data 
df = pd.read_excel("prez_data.xlsx")
presidents = sorted(df['Name'].unique())


st.title("🇺🇸 Talk Like a President")
st.markdown(
"""
Hi! Welcome to **Talk Like a President**.  
This app uses simple NLP to rewrite your sentence in the style of real U.S. Presidents, based on their **inaugural addresses** — whether they served one or two terms.

**How to use**
1. Choose a President from the dropdown.
2. Type any sentence.
3. Click **Translate**.

You’ll see:
- 🧱 **Basic Rewriter** — swaps vocabulary using that president’s inauguration speech.
- 🧠 **POS-Based Rewriter** — mimics grammar, structure, and tone inspired by their rhetoric.

*Educational demo — apolitical; not affiliated with any government or campaign.*
"""
)



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
