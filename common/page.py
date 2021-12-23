from common.element import BaseTextElement, LocationElement
from common.locators import LandingPageLocators as LPL


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver


class LandingPage(BasePage):

    def __init__(self, driver):
        super(LandingPage, self).__init__(driver)
        self.branches = {
            ("stammgelände", "morning"): LocationElement(driver, LPL.STAMMGELAENDE_MORNING),
            ("stammgelände", "evening"): LocationElement(driver, LPL.STAMMGELAENDE_EVENING),
        }

    def check_availability(self):
        return {name: b.availability for name, b in self.branches.items()}

    def click_reserve(self, branch_name: str, time: str):
        self._get_branch(branch_name, time).click_reserve()

    def _get_branch(self, branch_name: str, time: str):
        return self.branches.get((branch_name.lower(), time.lower()))


class BookingPage(BasePage):

    def __init__(self, driver):
        super(BookingPage, self).__init__(driver)




