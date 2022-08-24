"""This file is where most of the selenium is going on. Functions will
be made here to run through different pages in the billing process infor has.
"""


import json
import math
import time
import traceback

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from Utils import jsonUtils
from WebDriver import EnviromentSetUp
from secret import inforAccountLogin, inforAccountPassword


class billingOrders(EnviromentSetUp):
    """Enviroment setup allows for the web object to be passed around wihtout having to create a new web object with a new function.

    Args:
        EnviromentSetUp (_type_): web is being held here
    """

    def login(user: str, password: str) -> None:
        """starts the web selenium server and logs into infor on company 40. Ends up taking you to billing entry page
        Args:
            user (str): username for infor
            password (str): password for infor
        """
        try:

            # Setting up the Web object here
            EnviromentSetUp.setUp()
            web = EnviromentSetUp.web
            wait = WebDriverWait(web, 30)
            # In case a longer timeout is needed
            longerWait = WebDriverWait(web, 120)

            # This is the link for the billing page. Will require login to infor first.
            web.get("https://xisrv.stronghandtools.com/infor/d7de089b-7e09-4476-a5f5-80697edc7524?favoriteContext=arece.master&LogicalId=lid://infor.sx.1")
            signInUser: WebElement = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="userNameInput"]')))
            signInUser.send_keys(inforAccountLogin)
            signInPassword: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="passwordInput"]')))
            signInPassword.send_keys(inforAccountPassword)
            signInSubmit: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="submitButton"]')))
            signInSubmit.click()

            # Checking to see if the document management tab is open and closing it in case it interupts a click
            documentMng: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="body"]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]')))
            if ("expanded" in documentMng.get_attribute("class")):
                close: WebElement = wait.until(EC.element_to_be_clickable((
                    By.XPATH, '/html/body/div[2]/infor-mingle-shell/nav-menu/div/header/section[2]/drop-menu/div[1]/ul/li[5]/button')))
                close.click()

            # Entering the frame inside the infor website which is where all the action is
            wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "sxeweb_d7de089b-7e09-4476-a5f5-80697edc7524")))

            # Logging in to personal infor account
            inforUser: WebElement = longerWait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="signin-userid"]')))
            inforUser.send_keys(str(user))
            inforPassword: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="signin-password"]')))
            inforCompany: WebElement = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//*[@id="signin-company"]')))
            inforPassword.send_keys(str(password))
            inforCompany.send_keys("40")
            inforSubmit: WebElement = wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="sign-in-view"]/section/form/button')))
            inforSubmit.click()

            # ClearOpButton will not always appear. This tries to click that button,
            # Exception will check if the next page was met.
            try:
                clearOpButton: WebElement = wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'btn-modal-primary')))
                clearOpButton.click()
            except:
                try:
                    journalOkButton = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[3]/button[2]')))
                except:
                    raise

            print("\nLogged in!")

        except Exception:
            print("\nCould not login")
            raise

    def customerSetUp(checkNumber: float = 220824, amount: float = 123.24, customerNum: int = 40010) -> None:
        """This will set up the first page of the cash receipt entry.
        It is supposed to fill in the CHeck #, Amount,
        Customer # and click next to move on.

        Args:
            checkNumber (str): Check #
            amount (float): Amount .
            customerNum (int): Customer #.
        """

        # Setting up the Web object here
        web = EnviromentSetUp.web
        wait = WebDriverWait(web, 30)
        # In case a longer timeout is needed
        longerWait = WebDriverWait(web, 120)
        # For time.sleep
        transition = 2
        try:
            print("Setting up Customer!")
            # This will close the journal, fill in check #, amount, and then click
            journalOkButton: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[@class="modal-page-container"]/div/div[1]/form/div[3]/button[2]')))
            journalOkButton.click()
            time.sleep(transition)
            checkNumInput: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH,
                '/html/body/div[2]/div/div/div/section[3]/div/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/input')))
            checkNumInput.click()
            time.sleep(transition)
            checkNumInput.send_keys(checkNumber)
            time.sleep(transition)
            amountInput: WebElement = wait.until(EC.visibility_of_element_located(
                (By.XPATH,
                '/html/body/div[2]/div/div/div/section[3]/div/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div[1]/input')))
            amountInput.click()
            amountInput.clear()
            time.sleep(transition)
            amountInput.send_keys(amount)
            time.sleep(transition)
            nextButton: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                '/html/body/div[2]/div/div/div/section[3]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/button[2]')))
            nextButton.click()
            time.sleep(transition)  

            # Next the customer# will be inputted and next will be clicked
            customerNumInput: WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/section[3]/div/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div[5]/span/input')))
            customerNumInput.send_keys(customerNum)
            shipToInput:WebElement = wait.until(EC.element_to_be_clickable(
                (By.XPATH,'/html/body/div[2]/div/div/div/section[3]/div/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div[1]/span/input')))
            shipToInput.click()
            time.sleep(transition)
            nextButton.click()
            time.sleep(transition)
            print("Sucessfully setup customer!")
        except:
            traceback.print_exc()
            raise Exception("Previous Journal not closed, Timeout, or invalid inputs")
