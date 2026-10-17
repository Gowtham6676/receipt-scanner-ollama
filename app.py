import streamlit as st
import pandas as pd
from PIL import Image
from ollama_reader import read_receipt

st.title("Smart Receipt Scanner")
st.caption("Powered by a local Ollama vision model")

if "records" not in st.session_state:
    st.session_state.records = []

file = st.file_uploader("Upload a receipt", type=["jpg", "jpeg", "png"])

if file:
    image = Image.open(file)
    st.image(image, width=300)

    with st.spinner("Reading receipt..."):
        try:
            data = read_receipt(image)
        except Exception as e:
            st.error(f"Could not read the receipt: {e}")
            st.stop()

    st.write("Detected:", data)
    if st.button("Save"):
        st.session_state.records.append(data)

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df)
    st.bar_chart(df.groupby("category")["total"].sum())
    st.download_button("Download CSV", df.to_csv(index=False), "expenses.csv")