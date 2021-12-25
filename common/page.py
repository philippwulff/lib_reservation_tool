from common.element import BaseTextElement, LocationElement
from common.locators import LandingPageLocators as LPL


class BasePage(object):

    def __init__(self, driver):
        """Base element for web pages.

        Parameters
        ----------
        driver : selenium.webdriver
            The driver object used to interact with the web page.
        """
        self.driver = driver


class LandingPage(BasePage):
    """
    All methods that are supposed to act on:
    https://www.ub.tum.de/arbeitsplatz-reservieren
    """
    def __init__(self, driver):
        """See parent class."""
        super(LandingPage, self).__init__(driver)
        self.branches = {
            ("stammgelände", "morning"): LocationElement(driver, LPL.STAMMGELAENDE_MORNING),
            ("stammgelände", "evening"): LocationElement(driver, LPL.STAMMGELAENDE_EVENING),
        }

    def check_availability(self):
        """Checks which library branches have seats available.

        Returns
        -------
        dict of shape {"branch_name": True or False, ...} which includes the availability info for every branch.
        """
        return {name: b.is_available for name, b in self.branches.items()}

    def click_reserve(self, branch_name: str, time: str):
        """If available, this clicks on the reservation button on the web page for a given branch and time.

        Parameters
        ----------
        branch_name : str
            The name of the library branch. This must match the strings specified in the class definition.
        time : str
            The reservation time slot. This must match the strings specified in the class definition.

        Returns
        -------
        None
        """
        self._get_branch(branch_name, time).click_reserve()

    def _get_branch(self, branch_name: str, time: str):
        """Helper method for parsing the library name and time slot to the correct format."""
        return self.branches.get((branch_name.lower(), time.lower()))


class BookingPage(BasePage):
    """
    All methods that are supposed to act on pages like:
    https://www.ub.tum.de/reserve/378129719
    """
    def __init__(self, driver):
        """See parent class."""
        super(BookingPage, self).__init__(driver)

        self.name = BaseTextElement()




