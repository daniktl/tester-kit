import os
import re
from threading import Thread

import PySimpleGUI as sg
from selenium import webdriver

from constants import JS_HEADERS_SCRIPT
from utils import check_response_content_type
from utils.selenium import content_highlighting, scroll_to_element

URL_REGEX = re.compile(r"http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

DEFAULT_BODY_FONT = "Arial 14"
HEADER_FONT = "Arial 20 bold"

XPATH_FIELD_KEY = '-CURRENT-XPATH-'
JMES_FIELD_KEY = '-CURRENT-JMES-'
URL_FIELD_KEY = "-CURRENT-URL"
SITEMAP_FIELD_KEY = "-SITEMAP-"

CONTENT_TYPE_OUTPUT_FIELD = "-CONTENT-TYPE-"
SEARCH_OUTPUT_FIELD = "-SEARCH-OUTPUT-"

XPATH_EVENT = "Look up XPath"
JMES_EVENT = "Look up JMes"
GO_TO_EVENT = "Load page"
UPLOAD_FILE_EVENT = "Upload"

DEFAULT_ROW_HEIGHT = 1
DEFAULT_WIDE_COLUMN_WIDTH = 70
DEFAULT_TIGHT_COLUMN_WIDTH = 26
DEFAULT_EQUAL_COLUMN_WIDTH = 32  # for 3 equal columns

SIZE_WIDE = (DEFAULT_WIDE_COLUMN_WIDTH, DEFAULT_ROW_HEIGHT)
SIZE_TIGHT = (DEFAULT_TIGHT_COLUMN_WIDTH, DEFAULT_ROW_HEIGHT)
SIZE_EQUAL = (DEFAULT_EQUAL_COLUMN_WIDTH, DEFAULT_ROW_HEIGHT)


class TesterGUI:
    window: sg.Window = None
    driver: webdriver = None

    def __init__(self):
        self.window_title = "Tester Kit"
        self.cp = sg.cprint
        self._init_layout()
        self.urls = []

    def _init_layout(self):
        self.layout = [
            [sg.T("Dataset", font=HEADER_FONT)],
            [sg.Text("URL")],
            [
                sg.InputText(key=URL_FIELD_KEY, size=SIZE_WIDE),
                sg.Submit(GO_TO_EVENT, size=SIZE_TIGHT)],
            [
                sg.Text("Upload sitemap:"),
                sg.Text(size=(38, 1)),
                sg.FileBrowse(key=SITEMAP_FIELD_KEY, size=(20, 1)),
                sg.Submit(UPLOAD_FILE_EVENT, size=(20, 1))
            ],

            [sg.T("")],
            [sg.T("Search criteria", font=HEADER_FONT)],
            [sg.Text("XPath")],
            [
                sg.Multiline(size=SIZE_WIDE, key=XPATH_FIELD_KEY),
                sg.Submit(XPATH_EVENT, size=SIZE_TIGHT)
            ],
            [sg.Text("JMesPath")],
            [
                sg.Multiline(size=SIZE_WIDE, key=JMES_FIELD_KEY),
                sg.Submit(JMES_EVENT, size=SIZE_TIGHT)
            ],

            [sg.T("")],
            [sg.T("Output", font=HEADER_FONT)],
            [
                sg.Text("Content-Type:", size=SIZE_TIGHT, font="bold"),
                sg.Text(key=CONTENT_TYPE_OUTPUT_FIELD, size=SIZE_WIDE)
            ],
            [
                sg.Text("Search results:", size=SIZE_TIGHT, font="bold"),
                sg.Multiline(size=SIZE_WIDE, key=SEARCH_OUTPUT_FIELD)
            ],
            [sg.T("")],
            [sg.T("Navigation", font=HEADER_FONT)],
            [
                sg.Column([[sg.Button("Previous")]], size=SIZE_EQUAL),
                sg.VSeparator(),
                sg.Column(
                    [[sg.Text("Step"), sg.InputText(size=(30, 5))]],
                    size=SIZE_EQUAL
                ),
                sg.VSeparator(),
                sg.Column([[sg.Button("Next")]], size=SIZE_EQUAL)
            ],
        ]

    def _init_window(self):
        self.window = sg.Window(self.window_title, self.layout, font=DEFAULT_BODY_FONT)

    def _update_window(self, field_key: str, new_value: str):
        self.window[field_key].update(new_value)

    def _update_config_value(self, config_name, args):
        return

    def _upload_sitemap(self, filepath: str):
        if not os.path.exists(filepath):
            return
        with open(filepath, "r") as f:
            urls = (URL_REGEX.search(x) for x in f.read().splitlines())
        urls = [url_search.group(0) for url_search in urls if url_search]
        if urls:
            initial_url = urls[0]
            self._update_window(URL_FIELD_KEY, initial_url)
            self._go_to(initial_url)

    def _thread_go_to(self, url: str):
        url = url.strip()
        if not url.startswith("http"):
            url = "http://" + url
        self.driver.get(url)
        headers = self.driver.execute_script(JS_HEADERS_SCRIPT)
        content_type = check_response_content_type(headers)
        self._update_window(CONTENT_TYPE_OUTPUT_FIELD, content_type)
        # driver.find_elements_by_xpath()

    def _go_to(self, url: str):
        if not url:
            return
        Thread(target=self._thread_go_to, args=(url,)).start()

    def _look_for_xpath(self, xpath: str):
        if not (xpath and isinstance(xpath, str)):
            return
        xpath = xpath.strip()
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            if elements:
                scroll_to_element(self.driver, elements[0])
                for element in elements:
                    content_highlighting(self.driver, element)
                self._update_window(
                    SEARCH_OUTPUT_FIELD,
                    "\n-----\n".join([element.get_attribute('innerText') for element in elements])
                )

            else:
                self._update_window(SEARCH_OUTPUT_FIELD, "No results")
        except Exception as exp:
            self._update_window(SEARCH_OUTPUT_FIELD, str(exp))

    def run(self, driver: webdriver):
        self._init_window()
        self.driver = driver
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == GO_TO_EVENT:
                self._go_to(values[URL_FIELD_KEY])
            elif event == XPATH_EVENT:
                self._look_for_xpath(values[XPATH_FIELD_KEY])
            elif event == UPLOAD_FILE_EVENT:
                self._upload_sitemap(values[SITEMAP_FIELD_KEY])

        self.driver.quit()
        # to properly end the selenium session
        self.window.close()
