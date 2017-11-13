#!venv/bin/python3.4
import os
import time
import random
import pytest
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
LBL_SHOPPING_CART = "Shopping Cart"
PRODUCT_NAME = "Test-Driven Development with Python: Obey the Testing Goat: Using Django, Selenium, and JavaScript"
SEARCH_PLACEHOLDER = "Search..."
DANCE_WITH_DRAGON = "A Dance with Dragons (A Song of Ice and Fire)"
STRUTS_IN_ACTION = "Struts 2 in Action"
SLEEP_TIME = 3
WAIT_TIME = 5


def header(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        print("-" * 100)
        r = f(*args, **kwargs)
        return r
    return wrapped


@pytest.fixture
def driver_connection():
    # get the path of ChromeDriverServer
    dir = os.path.dirname(__file__)
    chrome_driver_path = dir + "/chromedriver"

    # create a new Chrome session
    driver = webdriver.Chrome(chrome_driver_path)
    driver.implicitly_wait(30)
    driver.set_window_position(0, 0)
    driver.set_window_size(1024, 600)
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
        print("  - Login button clicked")

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


@header
def test_navigation(driver_connection):
    print("{} test started @{}".format(LBL_NAVIGATION, datetime.today()))

    driver = driver_connection

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


@header
def test_bad_login_credentials(driver_connection):
    print("{} test started @{}".format(LBL_INVALID_CREDENTIALS, datetime.today()))

    driver = driver_connection

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
    print("  - Login button clicked")

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


@header
def test_successful_login(driver_connection):
    print("{} test started @{}".format(LBL_LOGIN, datetime.today()))
    driver = driver_connection

    if odoo_login(driver):
        print("  - Successfully logged in")
        passed = "Passed"
    else:
        print("  - Login unsuccessful")
        passed = "Failed"

    print("Test status: {}.".format(passed))
    time.sleep(SLEEP_TIME)
    driver.quit()


@header
def test_successful_logout(driver_connection):
    print("{} test started @{}".format(LBL_LOGOUT, datetime.today()))
    driver = driver_connection

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


@header
def test_create_inventory_product(driver_connection):
    print("{} test started @{}".format(LBL_INVENTORY, datetime.today()))
    driver = driver_connection

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
                print("  - Waited for Create button to be visible")

                time.sleep(SLEEP_TIME)

                driver.find_element(By.XPATH, '//button[contains(text(), "{0}")]'.format("Create")).click()
                print("  - Clicked Create button")

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
                        print("  - Clicked published button")
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


@header
def test_delete_inventory_product(driver_connection):
    print("{} test started @{}".format(LBL_DEL_INVENTORY, datetime.today()))
    driver = driver_connection

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
                print("  - Waited for Create button to be visible")

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

                        action_btn_action = ActionChains(driver)
                        action_btn_action.move_to_element(action_button)
                        action_btn_action.click(action_button)
                        action_btn_action.perform()

                        time.sleep(SLEEP_TIME)

                        try:
                            wait.until(EC.visibility_of_element_located(
                                (By.XPATH, '//button[contains(text(), "{0}")]/following-sibling::ul/li/a'.format("Action"))
                            ))

                            delete_button = driver.find_element(By.XPATH, '//button[contains(text(), "{0}")]/following-sibling::ul/li/a'.format("Action"))

                            delete_action = ActionChains(driver)
                            delete_action.move_to_element(delete_button)
                            delete_action.click(delete_button)
                            delete_action.perform()

                            time.sleep(SLEEP_TIME)

                            Alert(driver).accept()
                            print("  - Alert OK button clicked")
                            print("Test status: Passed.")
                            time.sleep(SLEEP_TIME)
                            driver.quit()
                        except TimeoutException:
                            print("Timed out while testing {} :4".format(LBL_DEL_INVENTORY))    
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


@header
def test_create_shopping_cart(driver_connection):
    print("{} test started @{}".format(LBL_SHOPPING_CART, datetime.today()))

    driver = driver_connection

    # navigate to the application home page
    driver.get(BASE_URL + "/")
    print("  - Home page browsed")
    driver.get(BASE_URL + "/shop")
    print("  - Shop page browsed")
    
    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'oe_search_box')))
        search_box_placeholder = driver.find_element_by_name("search").get_property('placeholder')
        print("  - Search box found")

        dance_with_dragon_link = driver.find_element(By.XPATH, '//a[contains(text(), "{}")]'.format(DANCE_WITH_DRAGON))

        if dance_with_dragon_link:
            print("  - Found the book :: '{0}'".format(DANCE_WITH_DRAGON))

        dance_with_dragon_action = ActionChains(driver)
        dance_with_dragon_action.move_to_element(dance_with_dragon_link)
        dance_with_dragon_action.click(dance_with_dragon_link)
        dance_with_dragon_action.perform()
        print("  - '{0}' book link clicked".format(DANCE_WITH_DRAGON))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), "{0}")]'.format(DANCE_WITH_DRAGON))))
            print("  - '{0}' book details page loaded".format(DANCE_WITH_DRAGON))
            qty = 2
            quantity = driver.find_element_by_name("add_qty")
            old_qty = quantity.get_property('value')
            quantity.clear()
            quantity.send_keys(qty)
            print("  - Quantity changed from {0} to {1}".format(old_qty, qty))
            time.sleep(SLEEP_TIME)

            add_cart_link = driver.find_element(By.ID, 'add_to_cart')
            add_cart_action = ActionChains(driver)
            add_cart_action.move_to_element(add_cart_link)
            add_cart_action.click(add_cart_link)
            add_cart_action.perform()
            print("  - 'Add to Cart' button clicked")

            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "{0}")]'.format("Process Checkout"))))
                print("  - 'Process Checkout' found")

                continue_shopping_btn = driver.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format("Continue Shopping"))

                continue_shopping_action = ActionChains(driver)
                continue_shopping_action.move_to_element(continue_shopping_btn)
                continue_shopping_action.click(continue_shopping_btn)
                continue_shopping_action.perform()
                print("  - 'Continue Shopping' button clicked")

                try:
                    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'oe_search_box')))
                    search_box_placeholder = driver.find_element_by_name("search").get_property('placeholder')
                    print("  - Search box found")

                    struts_in_action_link = driver.find_element(By.XPATH, '//a[contains(text(), "{}")]'.format(STRUTS_IN_ACTION))

                    if struts_in_action_link:
                        print("  - Found the book :: '{0}'".format(STRUTS_IN_ACTION))

                    struts_in_action_action = ActionChains(driver)
                    struts_in_action_action.move_to_element(struts_in_action_link)
                    struts_in_action_action.click(struts_in_action_link)
                    struts_in_action_action.perform()
                    print("  - '{0}' book link clicked".format(STRUTS_IN_ACTION))
                    
                    try:
                        wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), "{0}")]'.format(STRUTS_IN_ACTION))))
                        print("  - '{0}' book details page loaded".format(STRUTS_IN_ACTION))
                        qty = 3
                        quantity = driver.find_element_by_name("add_qty")
                        old_qty = quantity.get_property('value')
                        quantity.clear()
                        quantity.send_keys(qty)
                        print("  - Quantity changed from {0} to {1}".format(old_qty, qty))
                        time.sleep(SLEEP_TIME)

                        add_cart_link = driver.find_element(By.ID, 'add_to_cart')
                        add_cart_action = ActionChains(driver)
                        add_cart_action.move_to_element(add_cart_link)
                        add_cart_action.click(add_cart_link)
                        add_cart_action.perform()
                        print("  - 'Add to Cart' button clicked")

                        try:
                            wait.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "{0}")]'.format("Process Checkout"))))
                            print("  - 'Process Checkout' found")

                            process_checkout_btn2 = driver.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format("Process Checkout"))

                            process_checkout_action2 = ActionChains(driver)
                            process_checkout_action2.move_to_element(process_checkout_btn2)
                            process_checkout_action2.click(process_checkout_btn2)
                            process_checkout_action2.perform()
                            print("  - 'Process Checkout' button clicked")

                            try:
                                wait.until(EC.visibility_of_element_located((By.XPATH, '//h3[contains(text(), "{0}")]'.format("Billing Information"))))
                                print("  - Billing page loaded")

                                name = driver.find_element_by_name("name")
                                company = driver.find_element_by_name("street")
                                email = driver.find_element_by_name("email")
                                phone = driver.find_element_by_name("phone")
                                street = driver.find_element_by_name("street2")
                                city = driver.find_element_by_name("city")
                                zip = driver.find_element_by_name("zip")

                                name.send_keys("Selenium Testing")
                                print("  - Typed the billing name")
                                time.sleep(1)
                                company.send_keys("Titan Champs")
                                print("  - Typed the billing company name")
                                time.sleep(1)
                                email.send_keys("selenium@titanchamps.org")
                                print("  - Typed the billing email address")
                                time.sleep(1)
                                phone.send_keys("(800) 123-4567")
                                print("  - Typed the billing phone number")
                                time.sleep(1)
                                street.send_keys("123 University St")
                                print("  - Typed the billing street address")
                                time.sleep(1)
                                city.send_keys("Fullerton")
                                print("  - Typed the billing city")
                                time.sleep(1)
                                zip.send_keys("92831")
                                print("  - Typed billing zipcode")

                                country = driver.find_element_by_name('country_id')
                                for option in country.find_elements_by_tag_name('option'):
                                    if option.text.strip() == 'United States':
                                        option.click()
                                        print("  - Selected the billing Country")
                                        break
                                
                                time.sleep(SLEEP_TIME)

                                state = driver.find_element_by_name('state_id')
                                for option in state.find_elements_by_tag_name('option'):
                                    if option.text.strip() == 'California':
                                        option.click()
                                        print("  - Selected the billing State")
                                        break

                                confirm_link = driver.find_element_by_css_selector('a.a-submit')

                                confirm_link_acion = ActionChains(driver)
                                confirm_link_acion.move_to_element(confirm_link)
                                confirm_link_acion.click(confirm_link)
                                confirm_link_acion.perform()
                                print("  - 'Confirm' button clicked")

                                try:
                                    wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(), "{0}")]'.format("Validate Order"))))
                                    print("  - Validate Order page loaded")

                                    pay_now_btn = driver.find_element(By.XPATH, '//span[contains(text(), "{0}")]/ancestor::button'.format("Pay Now"))

                                    pay_now_btn_action = ActionChains(driver)
                                    pay_now_btn_action.move_to_element(pay_now_btn)
                                    pay_now_btn_action.click(pay_now_btn)
                                    pay_now_btn_action.perform()
                                    print("  - 'Pay Now' button clicked")

                                    try:
                                        wait.until(EC.visibility_of_element_located((By.XPATH, '//h2[contains(text(), "{0}")]'.format("Thank you for your order."))))
                                        print("  - Order complete")
                                        print("Test status: Passed.")
                                        time.sleep(SLEEP_TIME)
                                        driver.quit()
                                    except TimeoutException:
                                        print("Timed out while testing {} :9".format(LBL_SHOPPING_CART))
                                except TimeoutException:
                                    print("Timed out while testing {} :8".format(LBL_SHOPPING_CART))
                            except TimeoutException:
                                print("Timed out while testing {} :7".format(LBL_SHOPPING_CART))
                        except TimeoutException:
                            print("Timed out while testing {} :6".format(LBL_SHOPPING_CART))
                    except TimeoutException:
                        print("Timed out while testing {} :5".format(LBL_SHOPPING_CART))
                except TimeoutException:
                    print("Timed out while testing {} :4".format(LBL_SHOPPING_CART))
            except TimeoutException:
                print("Timed out while testing {} :3".format(LBL_SHOPPING_CART))
        except TimeoutException:
            print("Timed out while testing {} :2".format(LBL_SHOPPING_CART))
    except TimeoutException:
        print("Timed out while testing {} :1".format(LBL_SHOPPING_CART))
