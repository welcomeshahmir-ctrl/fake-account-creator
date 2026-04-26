import streamlit as st
import os
from playwright.sync_api import sync_playwright

st.title("🌐 Live Website Viewer (Final Stable Version)")

url = st.text_input("Enter Website URL")
run = st.button("Open Website")


# 🔥 AUTO FIX: ensures chromium is installed inside runtime
os.system("playwright install chromium")


def open_page(url):
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
        page.goto(url, timeout=60000)

        screenshot_path = "page.png"
        page.screenshot(path=screenshot_path, full_page=True)

        browser.close()
        return screenshot_path


if run and url:
    try:
        st.info("Loading website...")

        img = open_page(url)

        st.success("Page loaded successfully ✅")
        st.image(img)

    except Exception as e:
        st.error(f"Error: {e}")
