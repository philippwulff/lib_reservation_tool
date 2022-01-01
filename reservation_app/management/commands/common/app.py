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
        # TODO check which driver is installed
        self.driver = webdriver.Safari()
        self.web_adress = web_adress

    def nav_to_landing_page(self):
        self.driver.get(self.web_adress)

    def make_reservation(self, rs):
        branch_name = rs["branch_name"]
        time_slot = rs["time_slot"]
        full_name = rs["full_name"]
        tum_id = rs["tum_id"]
        tum_email = rs["tum_email"]

        info = {
            "success": False,
            "reservation_datetime": "",
        }

        try:
            self.nav_to_landing_page()
            landing = LandingPage(self.driver)
            is_available = landing.check_availability().get(branch_name)
            if is_available:
                landing.click_reserve(branch_name, time_slot)
                time.sleep(1)
                booking = BookingPage(self.driver)
                # TODO make booking
                info["success"] = True
                info["reservation_datetime"] = ...
            else:
                self._print(f"Branch {branch_name} is not available at time slot {time_slot}", bcolors.WARNING)
        except WebpageLocatorError as e:
            self._print(f"Ran into {e} (info: {e.args[0]})", bcolors.FAIL)

        return

    def _print(self, txt: str, color_code=None):
        txt = f"[{datetime.now():%d-%m-%Y %H:%M:%S}]" + txt
        if not color_code:
            print(txt)
        else:
            print(f"{color_code}{txt}{bcolors.ENDC}")

    def teardown(self):
        self.driver.close()