from selenium.webdriver.common.by import By


class LandingPageLocators:
    """
    CSS selectors for the landing page:
    https://www.ub.tum.de/arbeitsplatz-reservieren
    """

    # The library location elements (the rows)
    STAMMGELAENDE_MORNING = (By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > table > tbody > tr.odd.views-row-first")
    STAMMGELAENDE_EVENING = (By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > table > tbody > tr:nth-child(2)")
    MATH_INFO_MORNING = (By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > table > tbody > tr:nth-child(3)")
    MATH_INFO_EVENING = (By.CSS_SELECTOR, "#block-system-main > div > div > div.view-content > table > tbody > tr:nth-child(4)")

    # The column elements (these elements are relative to the row elements)
    BRANCH = (By.CSS_SELECTOR, "td.views-field-field-teilbibliothek")
    DATE = (By.CSS_SELECTOR, "td.views-field-field-tag")
    TIME = (By.CSS_SELECTOR, "td.views-field-field-zeitslot")
    RESERVE_BUTTON = (By.CSS_SELECTOR, "td.internlink")


class BookingPageLocators:
    """
    CSS selectors for the page where the form is filled out:
    https://www.ub.tum.de/reserve/378129719
    """

    # Reservation info
    BRANCH = (By.CSS_SELECTOR, "#node-33536 > div > ul > li.taxonomy-term-references.taxonomy-term-reference-0")
    DATE = (By.CSS_SELECTOR, "#node-33536 > div > div.field.field-name-field-tag.field-type-date.field-label-hidden > div > div > span")
    TIME = (By.CSS_SELECTOR, "#node-33536 > div > div.field.field-name-field-zeitslot.field-type-list-text.field-label-hidden > div > div")

    # Fields in the input form
    FULL_NAME_FIELD = (By.CSS_SELECTOR, "#edit-field-tn-name-und-0-value")
    EMAIL_FIELD = (By.CSS_SELECTOR, "#edit-anon-mail")
    IS_STUDENT_CHECKBOX = (By.CSS_SELECTOR, "#edit-field-stud-ma-und > div:nth-child(1) > label")
    IS_NOT_STUDENT_CHECKBOX = (By.CSS_SELECTOR, "#edit-field-stud-ma-und > div:nth-child(2) > label")
    TUM_ID_FIELD = (By.CSS_SELECTOR, "#edit-field-tum-kennung-und-0-value")
    READ_TERMS_OF_USE_CHECKBOX = (By.CSS_SELECTOR, "#edit-field-benutzungsrichtlinien-und")
    AGREE_DATA_PRIVACY_CHECKBOX = (By.CSS_SELECTOR, "#edit-field-datenschutzerklaerung > div > label")

    # Buttons
    REGISTER_BUTTON = (By.CSS_SELECTOR, "#edit-submit")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "#edit-cancel")
