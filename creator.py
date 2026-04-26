import streamlit as st
from playwright.sync_api import sync_playwright
from faker import Faker
import re

fake = Faker()

st.title("🧠 Smart Form Tester (Stable Cloud Version)")

url = st.text_input("🔗 Enter Website URL")
run = st.button("Start Test")


def generate_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password()
    }


def detect_and_fill(page, data):
    inputs = page.query_selector_all("input")

    filled = 0

    for inp in inputs:
        try:
            name = (inp.get_attribute("name") or "").lower()
            placeholder = (inp.get_attribute("placeholder") or "").lower()
            typ = (inp.get_attribute("type") or "").lower()

            text = name + placeholder + typ

            if re.search("first|fname", text):
                inp.fill(data["first_name"])
                filled += 1

            elif re.search("last|lname", text):
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


if run and url:
    data = generate_data()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        filled = detect_and_fill(page, data)

        # try submit
        try:
            page.click("button")
            submitted = True
        except:
            submitted = False

        st.write(f"Fields filled: {filled}")

        if submitted:
            st.success("Form submitted attempt done ✅")
        else:
            st.warning("Submit button not detected ⚠️")

        browser.close()
