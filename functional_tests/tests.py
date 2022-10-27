import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class TestProjectPage(StaticLiveServerTestCase):

    def setUp(self):
        service_object = Service("/Users/jakegowler/Downloads/chromedriver 2")
        # Talk about test instability in headless mode.
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

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

    def test_signup_error_mismatch_pass(self):
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

    def test_register_success_create_entry(self):
        # The user signs up successfully, then navigates to the create page, creates an entry and is navigated to the
        # created page.
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
        testInput = 'Lorem Ipsum'
        self.browser.find_element(By.XPATH, "//input[@name='title']").send_keys(testInput)
        self.browser.find_element(By.XPATH, "//input[@name='body']").send_keys('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        self.browser.find_element(By.XPATH, "//input[@name='url']").send_keys('https://www.lipsum.com/')
        self.browser.find_element(By.XPATH, "//input[@name='icon']").send_keys('/Users/jakegowler/Documents/Lorem-Ipsum.png')
        self.browser.find_element(By.XPATH, "//input[@value='Add entry']").click()
        assert testInput in self.browser.find_element(By.CSS_SELECTOR, "h1[align='center']").text

    def test_register_success_upvote_entry(self):
        # The user signs up successfully, then navigates to the create page, creates an entry, is navigated to the
        # created page, and then presses the upvote button.
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
        testInput = 'Lorem Ipsum'
        self.browser.find_element(By.XPATH, "//input[@name='title']").send_keys(testInput)
        self.browser.find_element(By.XPATH, "//input[@name='body']").send_keys('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        self.browser.find_element(By.XPATH, "//input[@name='url']").send_keys('https://www.lipsum.com/')
        self.browser.find_element(By.XPATH, "//input[@name='icon']").send_keys('/Users/jakegowler/Documents/Lorem-Ipsum.png')
        self.browser.find_element(By.XPATH, "//input[@value='Add entry']").click()
        assert testInput in self.browser.find_element(By.CSS_SELECTOR, "h1[align='center']").text
        self.browser.find_element(By.XPATH, "//button[normalize-space()='Upvote 1']").click()
        upvoteButton = self.browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-lg.btn-block").text
        assert "Upvote 2" in upvoteButton

    def test_register_success_create_entry_view_homepage(self):
        # The user signs up successfully, then navigates to the create page, creates an entry and is navigated to the
        # created page, and tries to view their creation on the homepage.
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
        testInput = 'Lorem Ipsum'
        self.browser.find_element(By.XPATH, "//input[@name='title']").send_keys(testInput)
        testBody = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        self.browser.find_element(By.XPATH, "//input[@name='body']").send_keys(testBody)
        self.browser.find_element(By.XPATH, "//input[@name='url']").send_keys('https://www.lipsum.com/')
        self.browser.find_element(By.XPATH, "//input[@name='icon']").send_keys('/Users/jakegowler/Documents/Lorem-Ipsum.png')
        self.browser.find_element(By.XPATH, "//input[@value='Add entry']").click()
        assert testInput in self.browser.find_element(By.CSS_SELECTOR, "h1[align='center']").text
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Home']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle
        assert testInput in self.browser.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[2]/h1[1]").text
        assert testBody[:100] in self.browser.find_element(By.XPATH, "//body/div[@class='container']/div[1]/div[2]/p[1]").text
        assert "Upvote 1" in self.browser.find_element(By.XPATH, "//button[normalize-space()='Upvote 1']").text

    def test_register_success_create_entry_view_click_upvote(self):
        # The user signs up successfully, then navigates to the create page, creates an entry and is navigated to the
        # created page, and tries to view their creation on the homepage, then clicks upvote on the homepage.
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
        testInput = 'Lorem Ipsum'
        self.browser.find_element(By.XPATH, "//input[@name='title']").send_keys(testInput)
        testBody = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        self.browser.find_element(By.XPATH, "//input[@name='body']").send_keys(testBody)
        self.browser.find_element(By.XPATH, "//input[@name='url']").send_keys('https://www.lipsum.com/')
        self.browser.find_element(By.XPATH, "//input[@name='icon']").send_keys('/Users/jakegowler/Documents/Lorem-Ipsum.png')
        self.browser.find_element(By.XPATH, "//input[@value='Add entry']").click()
        assert testInput in self.browser.find_element(By.CSS_SELECTOR, "h1[align='center']").text
        self.browser.find_element(By.XPATH, "//a[normalize-space()='Home']").click()
        landingTitle = self.browser.find_element(By.XPATH, "//h1[normalize-space()='Multi-User Journal']").text
        assert "Multi-User Journal" in landingTitle
        assert "Upvote 1" in self.browser.find_element(By.XPATH, "//button[normalize-space()='Upvote 1']").text
        self.browser.find_element(By.XPATH, "//button[normalize-space()='Upvote 1']").click()
        testInput = 'Lorem Ipsum'
        assert testInput in self.browser.find_element(By.CSS_SELECTOR, "h1[align='center']").text



