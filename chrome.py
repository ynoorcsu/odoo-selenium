#!venv/bin/python3.4
import os
import time
import random
from functools import wraps
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


BASE_URL = "http://bravojava.asuscomm.com:8069"
LBL_LOGOUT = "Logout"
LBL_LOGIN = "Login"
LBL_INVALID_CREDENTIALS = "Wrong login/password"
LBL_SUCCESS_LOGIN_MSG = "#Inbox"
LBL_NAVIGATION = "Navigation"
LBL_INVENTORY = "Create inventory product"
LBL_DEL_INVENTORY = "Delete inventory product"
PRODUCT_NAME = "Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript"
SLEEP_TIME = 3
WAIT_TIME = 5


def header_footer(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        print("-" * 100)
        r = f(*args, **kwargs)
        print("-" * 100)
        return r
    return wrapped


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
    print("  - Login page browsed")

    # setup wait time
    wait = WebDriverWait(driver, WAIT_TIME)

    # add manual wait
    time.sleep(SLEEP_TIME)

    try:
        # wait until the element is visible in the GUI
        wait.until(EC.visibility_of_element_located((By.NAME, 'login')))

        # get the login textbox
        login_field = driver.find_element_by_name("login")
        # enter username
        login_field.send_keys("bravo90503@yahoo.com")
        print("  - Username entered")

        # get the login textbox
        password_field = driver.find_element_by_name("password")
        # enter password
        password_field.send_keys("bravo90503")
        print("  - Password entered")

        # Find the submit button
        driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
        print("  - Login button pressed")

        try:
            # wait until the element is visible in the GUI
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'o_thread_title')))

            # find #Inbox text
            inbox_message = driver.find_element(By.XPATH, '//li[contains(text(), "{0}")]'.format('#Inbox')).text

            if inbox_message == LBL_SUCCESS_LOGIN_MSG:
                return True
            else:
                return False
        except TimeoutException:
            return False
    except TimeoutException:
        print("Couldn't find login")


@header_footer
def delete_inventory_product():
    print("{} test started @{}".format(LBL_DEL_INVENTORY, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        print("  - Successfully logged in")
        wait = WebDriverWait(driver, WAIT_TIME)

        driver.find_element(By.XPATH, '//span[contains(text(), "{0}") and @class="oe_menu_text"]'.format("Inventory")).click()
        print("  - Clicked Inventory in the top navigation")

        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(text(), "{0}") and @class="oe_secondary_menu_section"]'
                    .format("Inventory Control")
                )
            ))

            driver.find_element(By.XPATH, '//div[contains(text(), "{0}") and @class="oe_secondary_menu_section"]/following-sibling::ul/li/a/span'
                .format("Inventory Control")).click()
            print("  - Clicked Products under the Inventory Control navigation")
            
            try:
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//button[contains(text(), "{0}")]'.format("Create"))
                ))
                print("  - Waited for Create button to appear")

                try:
                    kanban_details = driver.find_element(By.XPATH, '//div[@class="oe_kanban_details"]/strong[contains(text(), "{0}")]'.format(PRODUCT_NAME))

                    time.sleep(SLEEP_TIME)

                    if kanban_details.text.strip() == PRODUCT_NAME:
                        print("  - Product name matched")
                        global_click_action = ActionChains(driver)
                        global_click_action.move_to_element(kanban_details)
                        global_click_action.click(kanban_details)
                        global_click_action.perform()
                        print("  - Clicked on the product")

                    try:
                        wait.until(EC.visibility_of_element_located(
                            (By.XPATH, '//button[contains(text(), "{0}")]'.format("Action"))
                        ))

                        action_button = driver.find_element(By.XPATH, '//button[contains(text(), "{0}")]'.format("Action"))
                        delete_button = driver.find_element(By.XPATH, '//button[contains(text(), "{0}")]/following-sibling::ul/li/a'.format("Action"))

                        delete_action = ActionChains(driver)
                        delete_action.move_to_element(action_button)
                        delete_action.click(action_button)
                        delete_action.click(delete_button)
                        delete_action.perform()

                        print("  - Selected Action -> Delete option")

                        Alert(driver).accept()

                        print("  - Alert OK button pressed")

                        print("Test status: Passed.")
                        time.sleep(SLEEP_TIME)
                        driver.quit()
                    except TimeoutException:
                        print("Timed out while testing {} :3".format(LBL_DEL_INVENTORY))    
                except NoSuchElementException:
                    print("There's no product named ", PRODUCT_NAME)
            except TimeoutException:
                print("Timed out while testing {} :2".format(LBL_DEL_INVENTORY))

        except TimeoutException:
            print("Timed out while testing {} :1".format(LBL_DEL_INVENTORY))
    else:
        print("{} test failed.".format(LBL_DEL_INVENTORY))


@header_footer
def create_inventory_product():
    print("{} test started @{}".format(LBL_INVENTORY, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        print("  - Successfully logged in")
        wait = WebDriverWait(driver, WAIT_TIME)

        driver.find_element(By.XPATH, '//span[contains(text(), "{0}") and @class="oe_menu_text"]'.format("Inventory")).click()
        print("  - Clicked Inventory in the top navigation")

        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(text(), "{0}") and @class="oe_secondary_menu_section"]'
                    .format("Inventory Control")
                )
            ))

            driver.find_element(By.XPATH, '//div[contains(text(), "{0}") and @class="oe_secondary_menu_section"]/following-sibling::ul/li/a/span'
                .format("Inventory Control")).click()
            print("  - Clicked Products under the Inventory Control navigation")
            
            try:
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//button[contains(text(), "{0}")]'.format("Create"))
                ))
                print("  - Waited for Create button to appear")

                time.sleep(SLEEP_TIME)

                driver.find_element(By.XPATH, '//button[contains(text(), "{0}")]'.format("Create")).click()
                print("  - Pressed Create button")

                time.sleep(SLEEP_TIME)
                
                try:
                    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oe_avatar")))
                    product_name = driver.find_element_by_id("oe-field-input-4")
                    product_name.send_keys(PRODUCT_NAME)
                    print("  - Typed product name")

                    driver.find_element_by_name("ufile").send_keys(os.getcwd()+"/images/selenium.jpg")
                    print("  - Uploaded product image")

                    el = driver.find_element_by_id('oe-field-input-14')
                    for option in el.find_elements_by_tag_name('option'):
                        if option.text.strip() == 'Consumable':
                            option.click()
                            print("  - Product Type: Comsumable selected")
                            break

                    product_price = driver.find_element_by_id("oe-field-input-20")
                    product_price.clear();
                    price = str(round(random.uniform(10.00, 20.00), 2))
                    product_price.send_keys(price)
                    print("  - Product price set to: ${0}".format(price))

                    driver.find_element(By.XPATH, '//div[@class="o_stat_info published"]/span[contains(text(), "{0}")]'.format("Not Published")).click()
                    print("  - Clicked on 'Not Published'")

                    try:
                        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[contains(text(),"{0}")]'.format("Not Published"))))
                        driver.find_element(By.XPATH, '//button[contains(text(),"{0}")]'.format("Not Published")).click()
                        print("  - Pressed published button")
                        print("Test status: Passed.")
                        time.sleep(SLEEP_TIME)
                        driver.quit()
                    except TimeoutException:
                        print("Timed out while testing {} :4".format(LBL_INVENTORY))

                except TimeoutException:
                    print("Timed out while testing {} :3".format(LBL_INVENTORY))

            except TimeoutException:
                print("Timed out while testing {} :2".format(LBL_INVENTORY))

        except TimeoutException:
            print("Timed out while testing {} :1".format(LBL_INVENTORY))
    else:
        print("{} test failed.".format(LBL_INVENTORY))


@header_footer
def test_successful_logout():
    print("{} test started @{}".format(LBL_LOGOUT, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        print("  - Successfully logged in")
        wait = WebDriverWait(driver, WAIT_TIME)

        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'oe_topbar_name')))
            driver.find_element(By.XPATH, '//span[@class="oe_topbar_name"]').click()
            print("  - Administrator drop down opened")
            time.sleep(SLEEP_TIME)
            driver.find_element(By.XPATH, '//a[@data-menu="logout"]').click()
            print("  - Logout clicked")

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


@header_footer
def test_successful_login():
    print("{} test started @{}".format(LBL_LOGIN, datetime.today()))
    driver = driver_connection()

    if odoo_login(driver):
        print("  - Successfully logged in")
        passed = "Passed"
    else:
        print("  - Login unsuccessful")
        passed = "Failed"

    print("Test status: {}.".format(passed))
    time.sleep(SLEEP_TIME)
    driver.quit()


@header_footer
def test_bad_login_credentials():
    print("{} test started @{}".format(LBL_INVALID_CREDENTIALS, datetime.today()))

    driver = driver_connection()

    # navigate to the application home page
    driver.get(BASE_URL + "/web/login")
    print("  - Login page browsed")

    # get the login textbox
    login_field = driver.find_element_by_name("login")
    # enter username
    login_field.send_keys("ynoor@csu.fullerton.edu")
    print("  - Username entered")

    # get the login textbox
    password_field = driver.find_element_by_name("password")
    # enter password
    password_field.send_keys("$0m3Str@nG3P@55wOrd")
    print("  - Password entered")

    # Find the submit button
    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
    print("  - Login button pressed")

    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger')))
        alert_danger = driver.find_element_by_class_name("alert-danger").text

        if alert_danger == LBL_INVALID_CREDENTIALS:
            passed = "Passed"
            print("  - Message retrieved")
        else:
            passed = "Failed"
            print("  - Couldn't find any message")

        print("Test status: {}.".format(passed))
        time.sleep(SLEEP_TIME)
        driver.quit()
    except TimeoutException:
        print("Timed out while testing {}".format(LBL_INVALID_CREDENTIALS))


@header_footer
def test_navigation():
    print("{} test started @{}".format(LBL_NAVIGATION, datetime.today()))

    driver = driver_connection()

    # navigate to the application home page
    driver.get(BASE_URL + "/")
    print("  - Home page browsed")
    driver.get(BASE_URL + "/shop")
    print("  - Shop page browsed")
    driver.get(BASE_URL + "/event")
    print("  - Event page browsed")
    driver.get(BASE_URL + "/page/contactus")
    print("  - Contact us page browsed")

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
    test_navigation()
    test_bad_login_credentials()
    test_successful_login()
    test_successful_logout()
    create_inventory_product()
    delete_inventory_product()
