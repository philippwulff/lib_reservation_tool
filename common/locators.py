from selenium.webdriver.common.by import By


class LandingPageLocators:
    """
    CSS selectors for the landing page:
    https://www.ub.tum.de/arbeitsplatz-reservieren
    """

    # The library location elements (the rows)
    STAMMGELAENDE_MORNING = (By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > table > tbody > tr.odd.views-row-first")
    STAMMGELAENDE_EVENING = (By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > table > tbody > tr:nth-child(2)")

    # The column elements (these elements are relative to the row elements)
    BRANCH = (By.CLASS_NAME, "views-field views-field-field-teilbibliothek")
    DATE = (By.CLASS_NAME, "views-field views-field-field-tag")
    TIME = (By.CLASS_NAME, "views-field views-field-field-zeitslot")
    RESERVE_BUTTON = (By.CLASS_NAME, "views-field views-field-views-conditional internlink")

