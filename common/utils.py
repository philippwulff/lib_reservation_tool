from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from sys import stderr


def safari_click(element):
    """Workaround to click an element. A bug in Safari prevents element.click() from performing an actual click."""
    element.send_keys(Keys.RETURN)


def element_not_found(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoSuchElementException:
            print("Runtime warning: Element not found.", file=stderr)
            return ""
    return wrapper