from selenium.webdriver.support.ui import WebDriverWait
from common.locators import LandingPageLocators, BookingPageLocators
from common import utils
from common.exceptions import WebpageLocatorError
from selenium.common.exceptions import NoSuchElementException


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


class BaseTextElement(object):
    """
    Base element class for text input fields.

    Idea from:
    https://selenium-python.readthedocs.io/page-objects.html#page-elements
    """
    def __init__(self, locator, driver):
        self.locator = locator
        self.driver = driver

    def __set__(self, value):
        """Sets the text to the value supplied"""
        WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        self.driver.find_element(*self.locator).clear()
        self.driver.find_element(*self.locator).send_keys(value)

    def __get__(self):
        """Gets the text of the specified object"""
        WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
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
        utils.safari_click(self.driver.find_element(*BookingPageLocators.IS_STUDENT_CHECKBOX))

    def check_all_boxes(self):
        """Checks boxes for terms of use and data privacy agreement."""
        utils.safari_click(self.driver.find_element(*BookingPageLocators.READ_TERMS_OF_USE_CHECKBOX))
        utils.safari_click(self.driver.find_element(*BookingPageLocators.AGREE_DATA_PRIVACY_CHECKBOX))

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

