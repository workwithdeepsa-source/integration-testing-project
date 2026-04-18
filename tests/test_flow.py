import time
from selenium.webdriver.common.by import By
from utils.driver_setup import get_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_complete_flow():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.saucedemo.com/")
        time.sleep(2)

        # LOGIN
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        time.sleep(1)

        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)

        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # ADD TO CART
        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        time.sleep(2)

        # CART
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()
        time.sleep(2)

        # CHECKOUT
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        time.sleep(2)

        wait.until(EC.url_contains("checkout-step-one"))

        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(2)

        driver.find_element(By.ID, "continue").click()
        time.sleep(2)

        # OVERVIEW
        wait.until(EC.url_contains("checkout-step-two"))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        time.sleep(3)

        # SUCCESS
        success = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert "Thank you" in success

        time.sleep(5)  # final pause

    finally:
        driver.quit()