import streamlit as st
import requests

st.title("🌐 Website Viewer (Streamlit Safe Mode)")

url = st.text_input("Enter URL")
run = st.button("Open")

if run and url:
    try:
        st.info("Fetching website...")

        response = requests.get(url, timeout=10)
        html = response.text

        st.success("Page loaded successfully ✅")

        st.code(html[:3000], language="html")

    except Exception as e:
        st.error(f"Error: {e}")
