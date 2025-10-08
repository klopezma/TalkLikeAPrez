import streamlit as st
import pandas as pd
from translator.pipeline import translate_text, clean

st.set_page_config(page_title="Talk Like a President", page_icon="🦅")

st.title("🗽 Talk Like a President")
st.write("Type your message and see how a President might say it!")

@st.cache_data
def load_speeches():
    df = pd.read_excel("prez_data.xlsx")
    df['clean'] = df['Text'].apply(clean)
    return df

speeches = load_speeches()

user_input = st.text_area("Enter a sentence:")
if st.button("Translate"):
    if user_input.strip():
        result = translate_text(user_input, speeches)
        st.success(result)
    else:
        st.warning("Please type something first!")

st.caption("Educational demo — not affiliated with any government or campaign.")
