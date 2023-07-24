import allure
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options


@allure.step("启动浏览器")
def get_webdriver(browser):
    match browser:
        case "edge":
            print("edge 初始化")
            return driver_init_Edge()

        case "chrome":
            return driver_init_Chrome()


def driver_init_Edge():
    service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(service=service, options=options)
    driver.maximize_window()
    return driver


def driver_init_Chrome():
    pass
