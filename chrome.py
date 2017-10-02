#!venv/bin/python3.4
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

BASE_URL = "http://bravojava.asuscomm.com:8069"
LBL_LOGOUT = "Logout"
LBL_LOGIN = "Login"
LBL_INVALID_CREDENTIALS = "Wrong login/password"
LBL_SUCCESS_LOGIN_MSG = "Congratulations, your inbox is empty"
LBL_NAVIGATION = "Navigation"
LBL_INVENTORY = "Create inventory product"
SLEEP_TIME = 3
WAIT_TIME = 5

def driver_connection():
    # get the path of ChromeDriverServer
    dir = os.path.dirname(__file__)
    chrome_driver_path = dir + "/chromedriver"

    # create a new Chrome session
    driver = webdriver.Chrome(chrome_driver_path)
    driver.implicitly_wait(30)
    driver.maximize_window()

    return driver

def odoo_login(driver):
    # navigate to the application home page
    driver.get(BASE_URL + "/web/login")

    # get the login textbox
    login_field = driver.find_element_by_name("login")
    # enter username
    login_field.send_keys("bravo90503@yahoo.com")

    # get the login textbox
    password_field = driver.find_element_by_name("password")
    # enter password
    password_field.send_keys("bravo90503")

    # Find the submit button
    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()

    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'o_thread_title')))
        inbox_message = driver.find_element_by_class_name("o_thread_title").text

        if inbox_message == LBL_SUCCESS_LOGIN_MSG:
            return True
        else:
            return False
    except TimeoutException:
        return False


def create_inventory_product():
    print("{} test started @{}".format(LBL_INVENTORY, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        wait = WebDriverWait(driver, WAIT_TIME)

        driver.find_element(By.XPATH, '//span[contains(text(), "{0}") and @class="oe_menu_text"]'.format("Inventory")).click()

        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(text(), "{0}") and @class="oe_secondary_menu_section"]'
                    .format("Inventory Control")
                )
            ))

            driver.find_element(By.XPATH, '//div[contains(text(), "{0}") and @class="oe_secondary_menu_section"]/following-sibling::ul/li/a/span'
                .format("Inventory Control")).click()
            
            try:
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//button[contains(text(), "{0}")]'.format("Create"))
                ))

                time.sleep(SLEEP_TIME)

                driver.find_element(By.XPATH, '//button[contains(text(), "{0}")]'.format("Create")).click()

                time.sleep(SLEEP_TIME)
                
                try:
                    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oe_avatar")))
                    product_name = driver.find_element_by_id("oe-field-input-4")
                    product_name.send_keys("Selenium")

                    el = driver.find_element_by_id('oe-field-input-14')
                    for option in el.find_elements_by_tag_name('option'):
                        if option.text.strip() == 'Consumable':
                            option.click()
                            break

                    time.sleep(SLEEP_TIME)
                    driver.quit()
                except TimeoutException:
                    print("Timed out while testing {} :3".format(LBL_INVENTORY))

            except TimeoutException:
                print("Timed out while testing {} :2".format(LBL_INVENTORY))

        except TimeoutException:
            print("Timed out while testing {} :1".format(LBL_INVENTORY))
    else:
        print("{} test failed.".format(LBL_INVENTORY))


def test_successfull_logout():
    print("{} test started @{}".format(LBL_LOGOUT, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        wait = WebDriverWait(driver, WAIT_TIME)

        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'oe_topbar_name')))
            driver.find_element(By.XPATH, '//span[@class="oe_topbar_name"]').click()
            time.sleep(SLEEP_TIME)
            driver.find_element(By.XPATH, '//a[@data-menu="logout"]').click()

            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit"]')))
                logout_text = driver.find_element(By.XPATH, '//button[@type="submit"]').text
                
                if logout_text == "Log in":
                    passed = "Passed"
                else:
                    passed = "Failed"

                print("Test status: {}.".format(passed))
                time.sleep(SLEEP_TIME)
                driver.quit()
            except TimeoutException:
                print("Timed out while testing {}".format(LBL_LOGOUT))
        except TimeoutException:
            print("Timed out while testing {}".format(LBL_LOGOUT))
    else:
        print("{} test failed.".format(LBL_LOGOUT))


def test_successfull_login():
    print("{} test started @{}".format(LBL_LOGIN, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        passed = "Passed"
    else:
        passed = "Failed"

    print("Test status: {}.".format(passed))
    time.sleep(SLEEP_TIME)
    driver.quit()


def test_bad_login_credentials():
    print("{} test started @{}".format(LBL_INVALID_CREDENTIALS, datetime.today()))

    driver = driver_connection()

    # navigate to the application home page
    driver.get(BASE_URL + "/web/login")

    # get the login textbox
    login_field = driver.find_element_by_name("login")
    # enter username
    login_field.send_keys("ynoor@csu.fullerton.edu")

    # get the login textbox
    password_field = driver.find_element_by_name("password")
    # enter password
    password_field.send_keys("$0m3Str@nG3P@55wOrd")

    # Find the submit button
    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()

    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger')))
        alert_danger = driver.find_element_by_class_name("alert-danger").text

        if alert_danger == LBL_INVALID_CREDENTIALS:
            passed = "Passed"
        else:
            passed = "Failed"

        print("Test status: {}.".format(passed))
        time.sleep(SLEEP_TIME)
        driver.quit()
    except TimeoutException:
        print("Timed out while testing {}".format(LBL_INVALID_CREDENTIALS))


def test_navigate():
    print("{} test started @{}".format(LBL_NAVIGATION, datetime.today()))

    driver = driver_connection()

    # navigate to the application home page
    driver.get(BASE_URL + "/")
    driver.get(BASE_URL + "/shop")
    driver.get(BASE_URL + "/event")
    driver.get(BASE_URL + "/page/contactus")

    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'mt64')))
        contact_us_text = driver.find_element_by_css_selector("div.mt64 a").text

        if contact_us_text == "Send us an email":
            passed = "Passed"
        else:
            passed = "Failed"

        print("Test status: {}.".format(passed))
        time.sleep(SLEEP_TIME)
        driver.quit()
    except TimeoutException:
        print("Timed out while testing {}".format(LBL_NAVIGATION))

if __name__ == "__main__":
    # test_navigate()
    # test_bad_login_credentials()
    # test_successfull_login()
    # test_successfull_logout()
    create_inventory_product()
