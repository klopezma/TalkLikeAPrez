import streamlit as st
import pandas as pd
import re
import csv
import os
from datetime import datetime
from translator.pipeline import rewrite, rewrite_pos, load_data

if not os.path.exists("usage_log.csv"):
    with open("usage_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "president", "sentence_length"])

df = pd.read_excel("prez_data.xlsx")
presidents = sorted(df['Name'].unique())

st.title("🇺🇸 Talk Like a President")

st.markdown(
"""
Hi! Welcome to my Talk Like a President NLP (Natural Language Processing) project.

This app uses simple NLP to rewrite your sentence in the style of real U.S. Presidents, based on their **inaugural addresses**, whether they served one or two terms.

**How to use**
1. Choose a President from the dropdown.
2. Type any sentence.
3. Click **Translate**.

You’ll see:
- 🧱 **Basic Rewriter** - swaps vocabulary using that president’s inauguration speech.
- 🧠 **POS-Based Rewriter** - mimics grammar, structure, and tone inspired by their rhetoric.

*Educational demo: apolitical; not affiliated with any government or campaign.*

Thank you for visiting my app!
"""
)

prezPick = st.selectbox("🎩 Choose a President", presidents)
sentence = st.text_area("💬 Enter what you'd like to rewrite:")

if st.button("Translate"):
    if sentence.strip():
        basic_output = rewrite(sentence, prezPick)
        pos_output = rewrite_pos(sentence, prezPick)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🧱 Basic Rewriter")
            st.success(basic_output)
        with col2:
            st.subheader("🧠 POS-Based Rewriter")
            st.info(pos_output)

        with open("usage_log.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                prezPick,
                len(sentence.split())
            ])
    else:
        st.warning("Please enter a sentence to translate.")

st.divider()
st.write("🔒 Admin Access")

admin_code = st.text_input("admin", type="password")

if admin_code == "vervuq-nuqja6-jujSon":
    if os.path.exists("usage_log.csv"):
        df_log = pd.read_csv("usage_log.csv")
        st.subheader("📊 Usage Data (Private View)")
        st.write(df_log.tail(10))
        st.bar_chart(df_log['president'].value_counts())
    else:
        st.write("No usage data yet.")
elif admin_code:
    st.error("Incorrect admin code.")
