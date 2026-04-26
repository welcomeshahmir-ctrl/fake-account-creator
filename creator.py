import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from faker import Faker
import time
import re

fake = Faker()

st.title("🧠 Smart Form Tester (Final Cloud Version)")

url = st.text_input("🔗 Enter Website URL")
run = st.button("Start Test")


# ===== DRIVER (NO CHROME DRIVER MANAGER) =====
def get_driver():
    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(options=options)


# ===== SMART DETECTION =====
def detect_field(element):
    name = (element.get_attribute("name") or "").lower()
    placeholder = (element.get_attribute("placeholder") or "").lower()
    typ = (element.get_attribute("type") or "").lower()

    text = name + " " + placeholder + " " + typ

    if re.search(r"first|fname|given", text):
        return "first_name"
    if re.search(r"last|lname|family", text):
        return "last_name"
    if re.search(r"mail|email", text):
        return "email"
    if re.search(r"pass|pwd", text):
        return "password"

    return None


# ===== FAKE DATA =====
def generate_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password()
    }


# ===== FILL FORM =====
def fill_form(driver):
    data = generate_data()
    inputs = driver.find_elements(By.TAG_NAME, "input")

    filled = 0

    for inp in inputs:
        try:
            field = detect_field(inp)

            if field:
                inp.clear()
                inp.send_keys(data[field])
                filled += 1
        except:
            continue

    return filled


# ===== SUBMIT =====
def submit_form(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            text = (btn.text or "").lower()

            if any(k in text for k in ["submit", "create", "sign", "register", "join"]):
                btn.click()
                return True

        if buttons:
            buttons[0].click()
            return True

    except:
        pass

    return False


# ===== RUN =====
if run and url:
    driver = get_driver()
    driver.get(url)

    time.sleep(3)

    st.info("Analyzing form... 🧠")

    try:
        filled = fill_form(driver)
        submitted = submit_form(driver)

        st.write(f"Fields detected & filled: {filled}")

        if submitted:
            st.success("Form submission attempted ✅")
        else:
            st.warning("Submit button not clearly detected ⚠️")

    except Exception as e:
        st.error(f"Error: {e}")

    driver.quit()
