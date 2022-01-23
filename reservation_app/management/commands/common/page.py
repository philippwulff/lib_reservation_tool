from reservation_app.management.commands.common.element import BookingFormElement, LocationElement
from reservation_app.management.commands.common.locators import LandingPageLocators as LPL
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from reservation_app.management.commands.common.exceptions import WebpageLocatorError


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

        locs = {
            "stammgelände": LPL.STAMMGELAENDE,
            "mathematik_informatik": LPL.MATH_INFO,
        }

        self.branches = {}
        for branch_name, loc in locs.items():
            try:
                rows = driver.find_elements(*loc)           # Two rows in the table
                self.branches[(branch_name, "morning")] = LocationElement(driver, rows[0])
                self.branches[(branch_name, "evening")] = LocationElement(driver, rows[1])
            except (NoSuchElementException, IndexError) as e:
                if isinstance(e, NoSuchElementException):
                    raise WebpageLocatorError(f"Could not find the 'location' row element in the table.", e)
                elif isinstance(e, IndexError):
                    raise WebpageLocatorError(f"Could not index the library elements.", e)

    def check_availability(self):
        """Checks which library branches have seats available.

        Returns
        -------
        dict of shape {"branch_name": True or False, ...} which includes the availability info for every branch.
        """
        return {keys: self.is_available(*keys) for keys, _ in self.branches.items()}

    def is_available(self, branch_name: str, time_slot: str):
        """Checks if a given branch is free during the time slot.

        Parameters
        ----------
        branch_name : str
            The name of the library branch.
        time_slot : str
            Either morning or evening
        Returns
        -------
        bool
        """
        return self.get_branch(branch_name, time_slot).is_available

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
        self.get_branch(branch_name, time).click_reserve()

    def get_reservation_datetime(self, branch_name: str, time_slot: str):
        """Returns the formatted datetime for the reservation.
        e.g., Montag, 03. Januar 2022 08:00 - 14:30
        """
        branch = self.get_branch(branch_name, time_slot)
        return f"{branch.date} {branch.time}"

    def get_branch(self, branch_name: str, time: str):
        """Helper method for parsing the library name and time slot to the correct format."""
        branch_keywords = {
            "stamm": "stammgelände",
            "math": "mathematik_informatik",
        }
        for key in branch_keywords:
            # e.g. if "stamm" is in "stammgelaende"
            if key in branch_name.lower():
                branch_name = branch_keywords[key]
        # "morning" may be "Morning"
        time = time.lower()
        return self.branches.get((branch_name, time))


class BookingPage(BasePage):
    """
    All methods that are supposed to act on pages like:
    https://www.ub.tum.de/reserve/378129719
    """
    def __init__(self, driver):
        """See parent class."""
        super(BookingPage, self).__init__(driver)
        self.booking_form = BookingFormElement(driver)

    def complete_reservation(self, full_name: str, email: str, tum_id: str):
        """Fills the booking form and clicks on 'Anmelden'.

        Parameters
        ----------
        full_name : str
        email : str
        tum_id : str
        is_student : bool
        """

        self.booking_form.full_name.set(full_name)
        self.booking_form.email.set(email)
        self.booking_form.tum_id.set(tum_id)
        self.booking_form.check_is_student()
        self.booking_form.check_all_boxes()
        # Finalize
        self.booking_form.click_register()
