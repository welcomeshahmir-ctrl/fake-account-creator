import streamlit as st
import os
from playwright.sync_api import sync_playwright

st.title("🌐 Stable Website Viewer (Auto Fix Version)")

url = st.text_input("Enter URL")
run = st.button("Open Website")


# 🔥 AUTO FIX: ensures browser is installed
os.system("playwright install chromium")


def open_page(target_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        page = browser.new_page()
        page.goto(target_url, timeout=60000)

        path = "page.png"
        page.screenshot(path=path, full_page=True)

        browser.close()
        return path


if run and url:
    try:
        st.info("Loading website...")

        img = open_page(url)

        st.success("Loaded successfully ✅")
        st.image(img)

    except Exception as e:
        st.error(f"Error: {e}")
