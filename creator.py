import streamlit as st
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="Website Viewer", layout="centered")

st.title("🌐 Website Viewer (Playwright + Streamlit)")

url = st.text_input("Enter Website URL")

run = st.button("Open Website")


def load_page(target_url):
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

        screenshot_path = "page.png"
        page.screenshot(path=screenshot_path, full_page=True)

        browser.close()
        return screenshot_path


if run:
    if not url:
        st.warning("Please enter a valid URL")
    else:
        try:
            st.info("Loading website... please wait")

            image_file = load_page(url)

            st.success("Page loaded successfully ✅")
            st.image(image_file, caption="Website Screenshot")

        except Exception as e:
            st.error(f"Error: {str(e)}")
