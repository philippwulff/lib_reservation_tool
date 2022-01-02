from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def safari_click(element):
    """Workaround to click an element. A bug in Safari prevents element.click() from performing an actual click."""
    element.send_keys(Keys.RETURN)


def javascript_click(driver, element):
    """From:
    https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click
    """
    driver.execute_script("arguments[0].click();", element)

def element_not_found(func):
    """Helper function to decorate getter methods for HTML element attributes. This catches the exception if an element
    is not found."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoSuchElementException:
            print(f"Runtime warning: Element not found: {func.__name__}.")
            return ""
    return wrapper
