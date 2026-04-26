import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import time
import re

fake = Faker()

st.title("🧠 Pro Smart Form Tester (AI-style detection)")

url = st.text_input("🔗 Enter Website URL")
run = st.button("Start Test")

# ===== DRIVER =====
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


# ===== SMART FIELD DETECTION =====
def detect_field_type(element):
    name = (element.get_attribute("name") or "").lower()
    placeholder = (element.get_attribute("placeholder") or "").lower()
    input_type = (element.get_attribute("type") or "").lower()

    text = name + " " + placeholder + " " + input_type

    if re.search(r"first|fname|given", text):
        return "first_name"
    if re.search(r"last|lname|family", text):
        return "last_name"
    if re.search(r"mail|email", text):
        return "email"
    if re.search(r"pass|pwd|password", text):
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


# ===== MAIN LOGIC =====
def fill_form(driver):
    data = generate_data()
    inputs = driver.find_elements(By.TAG_NAME, "input")

    mapped = 0

    for inp in inputs:
        try:
            field = detect_field_type(inp)

            if field:
                inp.clear()
                inp.send_keys(data[field])
                mapped += 1
        except:
            continue

    return mapped


def click_submit(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            text = (btn.text or "").lower()

            if any(k in text for k in ["submit", "sign", "create", "register", "join"]):
                btn.click()
                return True

        # fallback
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
        mapped = fill_form(driver)
        submitted = click_submit(driver)

        st.write(f"Fields detected & filled: {mapped}")

        if submitted:
            st.success("Form submission attempted ✅")
        else:
            st.warning("Submit button not clearly detected ⚠️")

    except Exception as e:
        st.error(f"Error: {e}")

    driver.quit()
