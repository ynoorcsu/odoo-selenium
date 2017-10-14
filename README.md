# odoo-selenium
Python scripts repo for testing following Odoo functionalities:
- Website navigation test.
- Bad credentials test.
- Successful login test.
- Successful logout test.
- Create inventory product test.
- Delete inventory product test.
- Shopping cart test.

# Prerequisites
- Python 3.4+
  - How to install python on Windows: http://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html
  - How to install python on Mac: http://www.macworld.co.uk/how-to/mac/coding-with-python-on-mac-3635912/
- pip
  - It should be already installed. Comes built-in with Python 3.4+ installation.
- Virtualenv
  -  How to install virtualenv: https://virtualenv.pypa.io/en/stable/installation/
- Git
- Chrome Browser
- Download OS Specific driver (ex: chromdriver, geckodriver) from: http://www.seleniumhq.org/download/

# Instruction to setup
- Read the manual: http://selenium-python.readthedocs.io/
- Once all the prerequisites are installed, please use git clone to copy the repo in your localbox.
- Activate the virtualenv in your terminal: `source venv/bin/active`
- Issue this command in your terminal: `chmod a+x chrome.py`
- Now run: `./chrome.py`

# Tests Conducted
### Navigation Test:
  ```
  Navigation test started
  - Home page browsed
  - Shop page browsed
  - Event page browsed
  - Contact us page browsed
  Test status: Passed.
  ```
### Bad login credentials test:
  ```
  Wrong login/password test started
  - Login page browsed
  - Username entered
  - Password entered
  - Login button pressed
  - Message retrieved
  Test status: Passed.
  ```
### Successful login test:
  ```
  Login test started
  - Login page browsed
  - Username entered
  - Password entered
  - Login button pressed
  - Successfully logged in
  Test status: Passed.
  ```
### Successful logout test:
  ```
  Logout test started
  - Login page browsed
  - Username entered
  - Password entered
  - Login button pressed
  - Successfully logged in
  - Administrator drop down opened
  - Logout clicked
  Test status: Passed.
  ```
### Create inventory product test:
  ```
  Create inventory product test started
  - Login page browsed
  - Username entered
  - Password entered
  - Login button pressed
  - Successfully logged in
  - Clicked Inventory in the top navigation
  - Clicked Products under the Inventory Control navigation
  - Waited for Create button to appear
  - Pressed Create button
  - Typed product name
  - Uploaded product image
  - Product Type: Comsumable selected
  - Product price set to: $15.19
  - Clicked on 'Not Published'
  - Pressed published button
  Test status: Passed.
  ```
### Delete inventory product test:
  ```
  Delete inventory product test started
  - Login page browsed
  - Username entered
  - Password entered
  - Login button pressed
  - Successfully logged in
  - Clicked Inventory in the top navigation
  - Clicked Products under the Inventory Control navigation
  - Waited for Create button to appear
  - Product name matched
  - Clicked on the product
  - Selected Action -> Delete option
  - Alert OK button pressed
  Test status: Passed.
  ```
### Shopping cart test:
  ```
  Shopping Cart test started
  - Home page browsed
  - Shop page browsed
  - Search box found
  - Found the book :: 'A Dance with Dragons (A Song of Ice and Fire)'
  - 'A Dance with Dragons (A Song of Ice and Fire)' book link clicked
  - 'A Dance with Dragons (A Song of Ice and Fire)' book details page loaded
  - Quantity changed from 1 to 2
  - 'Add to Cart' button pressed
  - 'Process Checkout' found
  - 'Continue Shopping' button pressed
  - Search box found
  - Found the book :: 'Struts 2 in Action'
  - 'Struts 2 in Action' book link clicked
  - 'Struts 2 in Action' book details page loaded
  - Quantity changed from 1 to 3
  - 'Add to Cart' button pressed
  - 'Process Checkout' found
  - 'Process Checkout' button pressed
  - Billing page loaded
  - Typed the billing name
  - Typed the billing company name
  - Typed the billing email address
  - Typed the billing phone number
  - Typed the billing street address
  - Typed the billing city
  - Typed billing zipcode
  - Selected the billing Country
  - Selected the billing State
  - 'Confirm' button pressed
  - Validate Order page loaded
  - 'Pay Now' button pressed
  - Order complete
  Test status: Passed.
  ```
