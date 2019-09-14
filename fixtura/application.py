from selenium import webdriver
from fixtura.session import SessionHelper
from fixtura.project import ProjectHelper
from fixtura.soap import SoapHelper


class Application:
    def __init__(self, browser, config):
        if browser == "firefox":
            self.wb = webdriver.Firefox()
        elif browser == "chrome":
            self.wb = webdriver.Chrome()
        elif browser == "ie":
            self.wb = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wb.implicitly_wait(4)
        self.soap = SoapHelper(self)
        self.session=SessionHelper(self)
        self.project=ProjectHelper(self)
        self.config = config
        self.base_url = config['web']['baseUrl']


    def is_not_valid(self):
        try:
            self.wb.current_url
            return False
        except:
            return True

    def open_home_page(self):
        wb = self.wb
        wb.get(self.base_url)

    def return_home_page(self):
        wb = self.wb
        if not (wb.current_url.endswith('/my_view_page.php') and len(wb.find_elements_by_class_name("form-title")) > 0):
            wb.find_element_by_link_text("My View").click()

    def destroy(self):
        wb = self.wb
        self.wb.quit()


