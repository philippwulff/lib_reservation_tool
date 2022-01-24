from selenium import webdriver
from reservation_app.management.commands.common.page import LandingPage, BookingPage
from reservation_app.management.commands.common.exceptions import WebpageLocatorError
import time
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'    # yellow
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class App:
    def __init__(self, web_adress: str):
        self.driver = self.config_driver()
        self.web_adress = web_adress

    def config_driver(self):
        """Checks which webdriver is installed and open the right one.

        Returns
        -------
        object from selenium.webdriver
        """
        for ith_retry in range(100):
            try:
                driver = webdriver.Safari()
                return driver
            except Exception as e:
                self._print(f"Webdriver Safari not available: {repr(e)}", color_code=bcolors.WARNING)
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                driver = webdriver.Chrome(options=chrome_options)
                self._print("Using webdriver Chrome.", color_code=bcolors.OKBLUE)
                return driver
            except Exception as e:
                self._print(f"Webdriver Chrome not available: {repr(e)}", color_code=bcolors.WARNING)
                print(e)
            time.sleep(10)
        raise Exception(f"Cannot launch a webdriver after {ith_retry} retries.")


    def reset(self, sleep=1):
        """Navigate to the landing page to reset the reservation process."""
        self.driver.get(self.web_adress)
        time.sleep(sleep)

    def is_same_date(self, landing, branch_name: str, time_slot: str, current_res: str):
        """If the currently open reservation matches the given reservation string.

        Parameters
        ----------
        landing : page.LandingPage
            The object tha wraps the landing page.
        branch_name : str
            The name of the library branch.
        time_slot : str
            Either morning or evening.
        current_res : str
            The current reservation string containing date and time
        Returns
        -------
        bool
        """
        element = landing.get_branch(branch_name, time_slot)
        if element.date == "" or element.time == "":
            raise WebpageLocatorError(f"The located element date or time for branch {branch_name} in time slot "
                                      f"{time_slot} were empty strings.")
        if element.date in current_res:
            if element.time in current_res:
                return True
        return False

    def make_reservation(self, rs: dict, current_reservation: str):
        branch_name = rs["branch_name"]
        time_slot = rs["time_slot"]
        full_name = rs["full_name"]
        tum_id = rs["tum_id"]
        tum_email = rs["tum_email"]

        info = {
            "already_reserved": False,
            "success": False,
            "reservation_datetime": "",
        }

        try:
            self.reset()
            landing = LandingPage(self.driver)      # can raise WebpageLocatorError
            # The currently open reservation has been made previously.
            if self.is_same_date(landing, branch_name, time_slot, current_reservation):
                info["already_reserved"] = True
                info["reservation_datetime"] = current_reservation
                return info
            # Cache this value, as the landing is no longer available, when navigating to 'booking'
            reservation_datetime = landing.get_reservation_datetime(branch_name, time_slot)
            # The reservation can be made.
            if landing.is_available(branch_name, time_slot):
                landing.click_reserve(branch_name, time_slot)
                time.sleep(1)
                booking = BookingPage(self.driver)
                booking.complete_reservation(full_name, tum_email, tum_id)
                info["success"] = True
                info["reservation_datetime"] = reservation_datetime
                self._print(f"Booked branch {branch_name} at time slot {time_slot} for user {full_name}.", bcolors.OKGREEN)
            # Fully booked.
            else:
                # self._print(f"Branch {branch_name} is not available at time slot {time_slot}", bcolors.WARNING, end="\r")
                pass
        # This is thrown in case of changes in the HTML and CSS of the reservation webpage.
        except WebpageLocatorError as e:
            self._print(f"Ran into {e} (info: {e.args[0]})", bcolors.FAIL)
            time.sleep(30)  # Wait for some time because there is some issue with the website
        return info

    # def parse_datetime(self, date: str, time: str):
    #
    #     return dt_str

    def _print(self, txt: str, color_code=None, end=None):
        txt = f"[{datetime.now():%d-%m-%Y %H:%M:%S}]" + txt
        if not color_code:
            print(txt)
        else:
            print(f"{color_code}{txt}{bcolors.ENDC}{' '*30}", end=end)

    def teardown(self):
        self.driver.close()