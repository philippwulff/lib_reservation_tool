from selenium.webdriver.support.ui import WebDriverWait
from reservation_app.management.commands.common.locators import LandingPageLocators, BookingPageLocators
from reservation_app.management.commands.common import utils
from reservation_app.management.commands.common.exceptions import WebpageLocatorError
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import sys


class LocationElement(object):
    reserve_str = "Zur Reservierung"

    def __init__(self, driver, locator: (str, str)):
        self.driver = driver
        try:
            self.parent = driver.find_element(*locator)
        except NoSuchElementException as e:
            raise WebpageLocatorError(f"Could not find the 'location' row element in the table.", e)
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
        # e.g. '\n             Montag, 03. Januar 2022          '
        date = self.parent.find_element(*LandingPageLocators.DATE).text
        date = date.lstrip().rstrip()
        # -> 'Montag, 03. Januar 2022'
        return date

    @property
    @utils.element_not_found
    def time(self):
        # e.g., '\n              08:00 – 14:30          '
        t = self.parent.find_element(*LandingPageLocators.TIME).text
        t = t.lstrip().rstrip()
        # -> '08:00 – 14:30'
        return t

    @property
    @utils.element_not_found
    def is_available(self):
        # Is something like '\n        Zur Reservierung          '
        return self.reserve_str in self.reserve_button.text

    def click_reserve(self):
        try:
            if self.is_available:
                # Click does not work on my machine
                self.driver.get(self.reserve_button.find_element((By.CSS_SELECTOR, "a")).get_attribute("href"))
                # utils.javascript_click(self.driver, self.reserve_button)
            else:
                print(f"No reservation possible for branch {self.branch} at date and time {self.date, self.time}.")
        except NoSuchElementException as e:
            raise WebpageLocatorError(f"Could not click on 'Zur Resevierung' for branch {self.branch} at "
                                      f"date and time {self.date, self.time}", e)


class BaseTextElement(object):
    """
    Base element class for text input fields.

    Idea from:
    https://selenium-python.readthedocs.io/page-objects.html#page-elements
    """
    def __init__(self, driver, locator):
        self.locator = locator
        self.driver = driver

    def set(self, value):
        """Sets the text to the value supplied"""
        try:
            WebDriverWait(self.driver, 1000).until(
                lambda driver: driver.find_element(*self.locator))
        except TimeoutException as e:
            print(f"Received TimeoutException when trying to set value '{value}'.", file=sys.stderr)
            return
        self.driver.find_element(*self.locator).clear()
        self.driver.find_element(*self.locator).send_keys(value)

    def get(self):
        """Gets the text of the specified object"""
        try:
            WebDriverWait(self.driver, 1000).until(
                lambda driver: driver.find_element(*self.locator))
        except TimeoutException as e:
            print(f"Received TimeoutException when trying to get value.", file=sys.stderr)
            return
        element = self.driver.find_element(*self.locator)
        return element.get_attribute("value")


class BookingFormElement(object):
    """
    This class incorporates all the elements from the from that the user needs to interact with when making a
    reservation.
    """
    def __init__(self, driver):
        self.driver = driver
        self.full_name = BaseTextElement(driver, BookingPageLocators.FULL_NAME_FIELD)
        self.email = BaseTextElement(driver, BookingPageLocators.EMAIL_FIELD)
        self.tum_id = BaseTextElement(driver, BookingPageLocators.TUM_ID_FIELD)

    def check_is_student(self):
        """Select that this reservation is made for a student"""
        utils.javascript_click(self.driver, self.driver.find_element(*BookingPageLocators.IS_STUDENT_CHECKBOX))

    def check_all_boxes(self):
        """Checks boxes for terms of use and data privacy agreement."""
        utils.javascript_click(self.driver, self.driver.find_element(*BookingPageLocators.READ_TERMS_OF_USE_CHECKBOX))
        utils.javascript_click(self.driver, self.driver.find_element(*BookingPageLocators.AGREE_DATA_PRIVACY_CHECKBOX))

    def click_register(self):
        """Clicks on 'Anmelden'."""
        self.driver.find_element(*BookingPageLocators.REGISTER_BUTTON).submit()

    @property
    @utils.element_not_found
    def branch(self):
        """The branch name."""
        return self.driver.find_element(*BookingPageLocators.BRANCH).text

    @property
    @utils.element_not_found
    def date(self):
        """Reservation date."""
        return self.driver.find_element(*BookingPageLocators.DATE).text

    @property
    @utils.element_not_found
    def time(self):
        """Reservation time slot."""
        return self.driver.find_element(*BookingPageLocators.TIME).text

