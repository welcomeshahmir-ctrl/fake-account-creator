from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import threading
import time

fake = Faker()

TOTAL_ACCOUNTS = 1000
THREADS = 5   # ⚠️ isko zyada na karo (5–10 safe range)
DELAY = 1

success = 0
failed = 0
lock = threading.Lock()

link = input("Enter website link: ")

def create_account(start, end):
    global success, failed

    driver = webdriver.Chrome()
    driver.get(link)

    for i in range(start, end):
        try:
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name}{i}@test.com"
            password = fake.password()

            # ⚠️ CHANGE selectors according to your site
            driver.find_element(By.NAME, "first_name").clear()
            driver.find_element(By.NAME, "first_name").send_keys(first_name)

            driver.find_element(By.NAME, "last_name").clear()
            driver.find_element(By.NAME, "last_name").send_keys(last_name)

            driver.find_element(By.NAME, "email").clear()
            driver.find_element(By.NAME, "email").send_keys(email)

            driver.find_element(By.NAME, "password").clear()
            driver.find_element(By.NAME, "password").send_keys(password)

            driver.find_element(By.XPATH, "//button").click()

            with lock:
                success += 1
                print(f"[{i}] Success ✅")

        except:
            with lock:
                failed += 1
                print(f"[{i}] Failed ❌")

        time.sleep(DELAY)
        driver.get(link)

    driver.quit()


# تقسیم work across threads
accounts_per_thread = TOTAL_ACCOUNTS // THREADS
threads = []

for i in range(THREADS):
    start = i * accounts_per_thread
    end = start + accounts_per_thread

    t = threading.Thread(target=create_account, args=(start, end))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n===== FINAL RESULT =====")
print("Total:", TOTAL_ACCOUNTS)
print("Success:", success)
print("Failed:", failed)
