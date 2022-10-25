from selenium import webdriver
from entries.models import Journal
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestProjectPage(StaticLiveServerTestCase):

    def setUp(self):
        service_object = Service("/Users/jakegowler/Downloads/chromedriver 2")
        self.browser = webdriver.Chrome(service=service_object)

    def tearDown(self):
        self.browser.close()

    def test_Opening_landing_page(self):
        # The user opens the landing page.
        self.browser.get(self.live_server_url)
        assert self.browser.title == "Learning journal app."
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle

    def test_home_button(self):
        # The presses the home button. - Only needed to be tested once due to HTML inheritance.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Home']").click()
        assert self.browser.title == "Learning journal app."
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle

    def test_signup_button(self):
        # The user requests the signup page from the landing page.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp

    def test_signup_error_no_details(self):
        # The user requests the signup page and enters no details.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp

    def test_signup_error_no_pass(self):
        # The user requests the signup page and enters only a username.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp

    def test_signup_error_no_confirm_pass(self):
        # The user requests the signup page and enters only a username and a password.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password1']").send_keys("password")
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp

    def test_signup_error_no_mismatch_pass(self):
        # The user requests the signup page and enters mismatching passwords.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password1']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@name='password2']").send_keys("Password")
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        passwordError = self.browser.find_element(By.XPATH, "//div[@class='container']").text
        assert "Passwords must " in passwordError

    def test_signup_success(self):
        # The user requests the signup page and enters matching passwords.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password1']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@name='password2']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle

    def test_login_button(self):
        # The user requests the login page from the landing page.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        login = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Login!']").text
        assert "Login!" in login

    def test_login_error_full_details(self):
        # The user unsuccessfully logs in and is presented with an error message.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        login = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Login!']").text
        assert "Login!" in login
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("test")
        self.browser.find_element(By.XPATH, "//input[@name='password']").send_keys("test")
        self.browser.find_element(By.XPATH, "//input[@value='Login']").click()
        errorMessage = self.browser.find_element(By.XPATH, "//div[@class='container']").text
        assert "Username or password is incorrect." in errorMessage

    def test_login_error_no_user(self):
        # The user unsuccessfully logs in with no username and is presented with an error message.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        login = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Login!']").text
        assert "Login!" in login
        self.browser.find_element(By.XPATH, "//input[@name='password']").send_keys("test")
        self.browser.find_element(By.XPATH, "//input[@value='Login']").click()
        errorMessage = self.browser.find_element(By.XPATH, "//div[@class='container']").text
        assert "Username or password is incorrect." in errorMessage

    def test_login_error_no_pass(self):
        # The user unsuccessfully logs in due to no password and is presented with an error message.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        login = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Login!']").text
        assert "Login!" in login
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("test")
        self.browser.find_element(By.XPATH, "//input[@value='Login']").click()
        errorMessage = self.browser.find_element(By.XPATH, "//div[@class='container']").text
        assert "Username or password is incorrect." in errorMessage

    def test_register_success_logout_success(self):
        # The user requests the signup page and enters matching passwords, then logs out.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password1']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@name='password2']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Logout']").click()
        loginButton = self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").text
        assert "Login" in loginButton

    def test_register_success_logout_login_success(self):
        # The user requests the signup page and enters matching passwords, then logs out, and wants to log back in.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password1']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@name='password2']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Logout']").click()
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        login = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Login!']").text
        assert "Login!" in login
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@value='Login']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle

    def test_register_success_navto_create(self):
        # The user signs up successfully, then navigates to the create page.
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Sign up']").click()
        signUp = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Sign up!']").text
        assert "Sign up!" in signUp
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        self.browser.find_element(By.XPATH, "//input[@name='username']").send_keys("tester")
        self.browser.find_element(By.XPATH, "//input[@name='password1']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@name='password2']").send_keys("password")
        self.browser.find_element(By.XPATH, "//input[@value='Sign up']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Create an entry']").click()
        createTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Share an entry.']").text
        assert "Share an entry." in createTitle

