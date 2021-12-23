from selenium.webdriver.support.ui import WebDriverWait
from common.locators import LandingPageLocators
from common import utils
from common.exceptions import WebpageLocatorError
from selenium.common.exceptions import NoSuchElementException


class BaseTextElement(object):
    """Base page class that is initialized on every page object class.

    From:
    https://selenium-python.readthedocs.io/page-objects.html#page-elements
    """
    locator = None

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    def __get__(self, obj):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        return element.get_attribute("value")


class LocationElement(object):
    reserve_str = "Zur Reservierung"

    def __init__(self, driver, locator: (str, str)):
        try:
            self.parent = driver.find_element(*locator)
        except NoSuchElementException as e:
            raise WebpageLocatorError("Could not find the row element.", e)
        try:
            self.reserve_button = self.parent.find_element(*LandingPageLocators.RESERVE_BUTTON)
        except NoSuchElementException as e:
            raise WebpageLocatorError("Could not find the 'Zur Reservierung' element.", e)

    @property
    @utils.element_not_found
    def branch(self):
        return self.parent.find_element(*LandingPageLocators.BRANCH).text

    @property
    @utils.element_not_found
    def date(self):
        return self.parent.find_element(*LandingPageLocators.DATE).text

    @property
    @utils.element_not_found
    def time(self):
        return self.parent.find_element(*LandingPageLocators.TIME).text

    @property
    @utils.element_not_found
    def is_available(self):
        return self.reserve_button.text == self.reserve_str

    def click_reserve(self):
        if self.is_available:
            utils.safari_click(self.reserve_button)
        else:
            print(f"No reservation possible for branch {self.branch} at date and time {self.date, self.time}.")
