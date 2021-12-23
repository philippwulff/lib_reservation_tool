from selenium import webdriver
from common.page import LandingPage, BookingPage
import time


class App:
    lp_adress = "https://www.ub.tum.de/arbeitsplatz-reservieren"

    def __init__(self):
        self.driver = webdriver.Safari()

    def refresh(self):
        self.driver.get(self.lp_adress)
        landing = LandingPage(self.driver)
        print(landing.check_availability())
        time.sleep(5)

    def teardown(self):
        self.driver.close()


if __name__ == "__main__":
    app = App()
    for i in range(3):
        app.refresh()
    app.teardown()