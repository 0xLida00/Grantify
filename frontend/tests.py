from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class HomePageTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    # Test: Home page loads with the correct header
    def test_homepage_loads(self):
        self.driver.get(self.live_server_url)
        header = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(header, "Welcome to Grantify")

    # Test: Login button redirects to the login page
    def test_login_button_redirects(self):
        self.driver.get(self.live_server_url)
        login_button = self.driver.find_element(By.LINK_TEXT, "Login")
        login_button.click()
        self.assertIn("/login/", self.driver.current_url)