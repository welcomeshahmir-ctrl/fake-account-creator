import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import threading
import time
import random

fake = Faker()

st.title("🚀 Auto Account Creator Tool")

# ===== ONLY 3 INPUTS =====
url = st.text_input("🔗 Enter Website Link")
total_accounts = st.number_input("🔢 Number of Accounts", 1, 5000, 100)
threads_count = st.number_input("🧵 Threads", 1, 10, 5)

start_btn = st.button("Start")

# ===== GLOBALS =====
success = 0
failed = 0
lock = threading.Lock()
used_emails = set()

progress = st.progress(0)
status = st.empty()


# ===== DRIVER =====
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # fast mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


# ===== SMART EMAIL GENERATOR =====
def generate_email(fn, ln, i):
    email = f"{fn.lower()}.{ln.lower()}{random.randint(1000,99999)}@gmail.com"

    while email in used_emails:
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1000,99999)}@gmail.com"

    used_emails.add(email)
    return email


# ===== WORKER =====
def worker(start, end):
    global success, failed

    driver = get_driver()
    driver.get(url)

    for i in range(start, end):
        try:
            fn = fake.first_name()
            ln = fake.last_name()
            pw = fake.password()

            email = generate_email(fn, ln, i)

            # AUTO FORM DETECTION (common fields)
            driver.find_element(By.NAME, "first_name").clear()
            driver.find_element(By.NAME, "first_name").send_keys(fn)

            driver.find_element(By.NAME, "last_name").clear()
            driver.find_element(By.NAME, "last_name").send_keys(ln)

            driver.find_element(By.NAME, "email").clear()
            driver.find_element(By.NAME, "email").send_keys(email)

            driver.find_element(By.NAME, "password").clear()
            driver.find_element(By.NAME, "password").send_keys(pw)

            driver.find_element(By.XPATH, "//button").click()

            with lock:
                success += 1

        except:
            with lock:
                failed += 1

        # update UI
        with lock:
            done = success + failed
            progress.progress(done / total_accounts)
            status.text(f"✅ Success: {success} | ❌ Failed: {failed}")

        time.sleep(1)
        driver.get(url)

    driver.quit()


# ===== RUN =====
if start_btn and url:
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

    st.success(f"Done 🎉 Success: {success} | Failed: {failed}")
