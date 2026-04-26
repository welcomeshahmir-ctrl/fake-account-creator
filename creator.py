import streamlit as st
from playwright.sync_api import sync_playwright
from faker import Faker
import re

fake = Faker()

st.title("🧠 Smart QA Form Tester (Playwright Cloud Safe)")

url = st.text_input("🔗 Enter Test URL")
run = st.button("Run Test")


# =====================
# DATA GENERATION
# =====================
def generate_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password()
    }


# =====================
# SMART FIELD DETECTION
# =====================
def detect_and_fill(page, data):
    inputs = page.query_selector_all("input")
    filled = 0

    for inp in inputs:
        try:
            name = (inp.get_attribute("name") or "").lower()
            placeholder = (inp.get_attribute("placeholder") or "").lower()
            typ = (inp.get_attribute("type") or "").lower()

            text = name + " " + placeholder + " " + typ

            if re.search(r"first|fname|given", text):
                inp.fill(data["first_name"])
                filled += 1

            elif re.search(r"last|lname|family", text):
                inp.fill(data["last_name"])
                filled += 1

            elif "email" in text:
                inp.fill(data["email"])
                filled += 1

            elif "pass" in text:
                inp.fill(data["password"])
                filled += 1

        except:
            continue

    return filled


# =====================
# MAIN RUN
# =====================
if run and url:
    st.info("Running Playwright test...")

    data = generate_data()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()
            page.goto(url, timeout=60000)

            filled = detect_and_fill(page, data)

            # try submit
            try:
                page.click("button")
                submitted = True
            except:
                submitted = False

            browser.close()

        st.write(f"Fields filled: {filled}")

        if submitted:
            st.success("Submit attempted successfully ✅")
        else:
            st.warning("Submit button not clearly detected ⚠️")

    except Exception as e:
        st.error(f"Error: {e}")
