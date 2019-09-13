from selenium.webdriver.support.select import Select
from model.project import Project
import re

class ProjectHelper:
    def __init__(self,app):
        self.app=app

    def add_new(self, project):
        wb = self.app.wb
        self.app.return_home_page()
        self.open_manage_page()
        self.open_manage_projects_page()
        wb.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_project_form(project)
        wb.find_element_by_css_selector("input[value='Add Project']").click()
        self.app.return_home_page()
        self.project_cache = None

    def open_manage_page(self):
        wb = self.app.wb
        wb.find_element_by_link_text("Manage").click()

    def open_manage_projects_page(self):
        wb = self.app.wb
        wb.find_element_by_link_text("Manage Projects").click()

    def select_contact_by_name(self, name):
        wb = self.app.wb
        wb.find_element_by_link_text(name).click()

    def delete_project_by_name(self, name):
        wb = self.app.wb
        self.app.return_home_page()
        self.open_manage_page()
        self.open_manage_projects_page()
        self.select_contact_by_name(name)
        # submit deletion
        wb.find_element_by_css_selector("input[value='Delete Project']").click()
        wb.implicitly_wait(5)
        wb.find_element_by_css_selector("input[value='Delete Project']").click()
        self.contact_cache = None

    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wb = self.app.wb
        if text is not None:
            wb.find_element_by_name(field_name).click()
            wb.find_element_by_name(field_name).clear()
            wb.find_element_by_name(field_name).send_keys(text)


    project_cache = None











