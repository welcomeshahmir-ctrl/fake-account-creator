import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import time

fake = Faker()

st.title("🧪 Universal Form Tester (Safe QA Tool)")

url = st.text_input("🔗 Website URL")
run = st.button("Start Test")

success = 0
failed = 0

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def generate_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password()
    }

def auto_fill(driver):
    data = generate_data()

    inputs = driver.find_elements(By.TAG_NAME, "input")

    for inp in inputs:
        try:
            name = inp.get_attribute("name") or ""
            placeholder = inp.get_attribute("placeholder") or ""

            field = (name + placeholder).lower()

            if "first" in field:
                inp.send_keys(data["first_name"])

            elif "last" in field:
                inp.send_keys(data["last_name"])

            elif "mail" in field:
                inp.send_keys(data["email"])

            elif "pass" in field:
                inp.send_keys(data["password"])

        except:
            continue

def click_button(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        if buttons:
            buttons[0].click()
            return True
    except:
        return False


if run and url:
    driver = get_driver()
    driver.get(url)

    time.sleep(3)

    try:
        auto_fill(driver)
        clicked = click_button(driver)

        if clicked:
            st.success("Form Submitted Attempted ✅")
        else:
            st.warning("Button not found ⚠️")

    except Exception as e:
        st.error(f"Error: {e}")

    driver.quit()
