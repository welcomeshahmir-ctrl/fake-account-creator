from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time

fake = Faker()

TOTAL_ACCOUNTS = 1000
DELAY = 2   # seconds between requests (important!)

success = 0
failed = 0

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

link = input("Enter website link: ")
driver.get(link)

for i in range(TOTAL_ACCOUNTS):
    try:
        # Generate unique data
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}{i}@test.com"   # ensure unique
        password = fake.password()

        # Fill form (CHANGE selectors according to your site)
        wait.until(EC.presence_of_element_located((By.NAME, "first_name"))).clear()
        driver.find_element(By.NAME, "first_name").send_keys(first_name)

        driver.find_element(By.NAME, "last_name").clear()
        driver.find_element(By.NAME, "last_name").send_keys(last_name)

        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys(email)

        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys(password)

        # Submit
        driver.find_element(By.XPATH, "//button").click()

        # Wait for success indicator (adjust this!)
        time.sleep(2)

        success += 1
        print(f"[{i+1}] Success ✅")

    except Exception as e:
        failed += 1
        print(f"[{i+1}] Failed ❌")

    # Small delay to avoid overload
    time.sleep(DELAY)

    # OPTIONAL: reload page if needed
    driver.get(link)

driver.quit()

print("\n===== RESULT =====")
print("Total:", TOTAL_ACCOUNTS)
print("Success:", success)
print("Failed:", failed)
