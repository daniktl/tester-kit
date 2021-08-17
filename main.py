from selenium import webdriver

from gui import TesterGUI


def main():
    driver = webdriver.Chrome(executable_path='etc/chromedriver')
    tester_gui = TesterGUI()
    tester_gui.run(driver)


if __name__ == '__main__':
    main()
