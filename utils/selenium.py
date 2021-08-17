from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from constants import HIGHLIGHT_STYLE, JS_SET_ATTRIBUTE_VALUE, HIGHLIGHT_CLASS_NAME, STYLES_INSERT_SCRIPT, JS_CLASS_ACTION_SCRIPT


def add_highlight_styling(driver: webdriver) -> None:
    driver.execute_script(STYLES_INSERT_SCRIPT)


def reset_content_highlighting(driver: webdriver) -> None:
    elements = driver.find_elements_by_css_selector(f".{HIGHLIGHT_CLASS_NAME}")
    for element in elements:
        driver.execute_script(JS_SET_ATTRIBUTE_VALUE, element, "class", "")


def content_highlighting(driver: webdriver, element) -> None:
    # driver.execute_script(JS_CLASS_ACTION_SCRIPT.format(action="add"), element, HIGHLIGHT_CLASS_NAME)
    driver.execute_script(JS_SET_ATTRIBUTE_VALUE, element, "style", HIGHLIGHT_STYLE)
    # driver.execute_script(JS_SET_ATTRIBUTE_VALUE, element, "class", HIGHLIGHT_CLASS_NAME)


def scroll_to_element(driver: webdriver, element) -> None:
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
