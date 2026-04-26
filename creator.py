import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import threading
import time

fake = Faker()

st.title("🚀 Bulk Account Creator (Testing Tool)")

# UI Inputs
url = st.text_input("Enter Website URL")
total_accounts = st.number_input("Total Accounts", 1, 5000, 100)
threads_count = st.number_input("Threads", 1, 10, 5)
delay = st.number_input("Delay (seconds)", 0.0, 5.0, 1.0)

st.markdown("### Form Field Names (change according to site)")
first_name_field = st.text_input("First Name Field", "first_name")
last_name_field = st.text_input("Last Name Field", "last_name")
email_field = st.text_input("Email Field", "email")
password_field = st.text_input("Password Field", "password")

start_button = st.button("Start")

# Shared variables
success = 0
failed = 0
lock = threading.Lock()

progress_bar = st.progress(0)
status_text = st.empty()


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # faster
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


def generate_user(index):
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": f"user{index}@test.com",
        "password": fake.password()
    }


def worker(start, end):
    global success, failed

    driver = get_driver()
    driver.get(url)

    for i in range(start, end):
        try:
            data = generate_user(i)

            driver.find_element(By.NAME, first_name_field).clear()
            driver.find_element(By.NAME, first_name_field).send_keys(data["first_name"])

            driver.find_element(By.NAME, last_name_field).clear()
            driver.find_element(By.NAME, last_name_field).send_keys(data["last_name"])

            driver.find_element(By.NAME, email_field).clear()
            driver.find_element(By.NAME, email_field).send_keys(data["email"])

            driver.find_element(By.NAME, password_field).clear()
            driver.find_element(By.NAME, password_field).send_keys(data["password"])

            driver.find_element(By.XPATH, "//button").click()

            with lock:
                success += 1

        except:
            with lock:
                failed += 1

        with lock:
            done = success + failed
            progress_bar.progress(done / total_accounts)
            status_text.text(f"✅ Success: {success} | ❌ Failed: {failed}")

        time.sleep(delay)
        driver.get(url)

    driver.quit()


if start_button and url:
    success = 0
    failed = 0

    threads = []
    per_thread = total_accounts // threads_count

    for i in range(threads_count):
        start = i * per_thread
        end = start + per_thread

        t = threading.Thread(target=worker, args=(start, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    st.success(f"Done! ✅ Success: {success}, ❌ Failed: {failed}")
