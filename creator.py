from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import threading
import time

# ===== CONFIG =====
URL = input("Enter website link: ")
TOTAL_ACCOUNTS = 1000
THREADS = 5
DELAY = 1

FIELDS = {
    "first_name": "first_name",
    "last_name": "last_name",
    "email": "email",
    "password": "password"
}

fake = Faker()

success = 0
failed = 0
lock = threading.Lock()


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # enable for faster

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def generate_user(index):
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": f"user{index}@test.com",
        "password": fake.password()
    }


def log_result(message):
    with open("results.txt", "a") as f:
        f.write(message + "\n")


def worker(start, end):
    global success, failed

    driver = get_driver()
    driver.get(URL)

    for i in range(start, end):
        try:
            data = generate_user(i)

            driver.find_element(By.NAME, FIELDS["first_name"]).clear()
            driver.find_element(By.NAME, FIELDS["first_name"]).send_keys(data["first_name"])

            driver.find_element(By.NAME, FIELDS["last_name"]).clear()
            driver.find_element(By.NAME, FIELDS["last_name"]).send_keys(data["last_name"])

            driver.find_element(By.NAME, FIELDS["email"]).clear()
            driver.find_element(By.NAME, FIELDS["email"]).send_keys(data["email"])

            driver.find_element(By.NAME, FIELDS["password"]).clear()
            driver.find_element(By.NAME, FIELDS["password"]).send_keys(data["password"])

            driver.find_element(By.XPATH, "//button").click()

            with lock:
                success += 1
                print(f"[{i}] Success ✅")
                log_result(f"{i} SUCCESS")

        except Exception as e:
            with lock:
                failed += 1
                print(f"[{i}] Failed ❌")
                log_result(f"{i} FAILED")

        time.sleep(DELAY)
        driver.get(URL)

    driver.quit()


# ===== THREADING =====
accounts_per_thread = TOTAL_ACCOUNTS // THREADS
threads = []

for i in range(THREADS):
    start = i * accounts_per_thread
    end = start + accounts_per_thread

    t = threading.Thread(target=worker, args=(start, end))
    threads.append(t)
    t.start()

for t in threads:
    t.join()


# ===== RESULT =====
print("\n===== FINAL RESULT =====")
print("Total:", TOTAL_ACCOUNTS)
print("Success:", success)
print("Failed:", failed)
