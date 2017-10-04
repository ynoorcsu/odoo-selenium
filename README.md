# odoo-selenium
Python scripts repo for testing following Odoo functionalities:
- Website navigation test.
- Bad credentials test.
- Successful login test.
- Successful logout test.
- Create inventory product test.
- Delete inventory product test.

# Prerequisites
- Python 3.4+
- Virtualenv
- Git
- Chrome Browser
- Download OS Specific driver (ex: chromdriver, geckodriver) from: http://www.seleniumhq.org/download/

# Instruction to setup
- Read the manual: http://selenium-python.readthedocs.io/
- Once all the prerequisites are installed, please use git clone to copy the repo in your localbox.
- Activate the virtualenv in your terminal: `source venv/bin/active`
- Issue this command in your terminal: `chmod a+x chrome.py`
- Now run: `./chrome.py`