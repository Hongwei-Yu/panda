import time
from typing import Optional

import unittest
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.remote.webdriver import WebElement as RemoteWebElement
from selenium.webdriver.support.wait import WebDriverWait

from src.base.models import BaseTestCase


class KeyWord:
    _all_keyword = None
    _activate_ele: RemoteWebElement = None
    webdriver: RemoteWebDriver = None

    def __init__(self, webdriver: RemoteWebDriver):
        self.webdriver = webdriver
        self.save_value ={}

    def find_element(self, value: str) -> RemoteWebElement:
        return WebDriverWait(self.webdriver, 10, 5).until(
            lambda x: self.webdriver.find_element(By.XPATH, value)
        )

    def key_goto(self, step):
        self.webdriver.get(step.param)



    def key_touch(self,step):
        ele = self.find_element(step.ele_path)

    def key_click(self, step):
        ele = self.find_element(step.ele_path)

        ele.click()

    def key_input(self, step):
        ele = self.find_element(step.ele_path)

        ele.clear()
        ele.send_keys(step.param)

    def key_getSave(self,step):
        ele = self.find_element(step.ele_path)
        self.save_value[step.param] = ele.text

    def key_inputSave(self,step):
        ele = self.find_element(step.ele_path)
        ele.clear()
        ele.send_keys(self.save_value[step.param])
        time.sleep(3)
    def key_verify(self, step):
        time.sleep(5)
        validator = Validator(self,
                              step.ele_path,
                              step.verify_kw,
                              step.verify_exp,
                              step.param,
                              # args,
                              )
        validator.is_valid()


class Validator:

    def __init__(
            self,
            keyword: KeyWord,
            locator: Optional[str],
            verify_name: str,
            expression: str,
            value: str,
            # args: tuple,
    ):
        self.keyword = keyword
        self.locator = locator
        self.verify_name = verify_name
        self.expression = expression
        self.value = value
        # self.args = args

    def is_valid(self):

        a = self.get_actual_value()
        b = self.value

        if self.expression in [">", ">=", "<", "<=", "==", "!="]:
            # 常用表达式
            _ = f"a  {self.expression}  b "
            assert eval(_), f"断言失败： {_}"
        else:
            # 特殊表达式
            match self.expression:
                case "contains":
                    assert b in a, f"断言失败:  {a} contains {b}"
                case _:
                    raise ValueError(f"未知的验证表达式：{self.expression}")

    def get_actual_value(self):

        ele = None
        f = getattr(self, f"get_{self.verify_name}", None)
        if not f:
            ele = self.keyword.find_element(self.locator)
            f = getattr(self, f"get_ele_{self.verify_name}")

        return f(ele)

    def get_title(self, _: None):
        return self.keyword.webdriver.title

    def get_url(self, _: None):
        return self.keyword.webdriver.current_url

    def get_alert(self, _: None):
        return Alert(self.keyword.webdriver).text

    @staticmethod
    def get_ele_text(ele: RemoteWebElement):
        return ele.text

class Runner:

    def __init__(self, case: BaseTestCase):
        self.case = case
        self.__name__ = self.case.info.testcase_name
        self.__doc__ = ""

    def run(self, test: unittest.TestCase):
        webdriver: RemoteWebDriver = test.driver
        action = KeyWord(webdriver)

        for index, step in enumerate(self.case.steps, start=1):
            step_func = getattr(action, f"key_{step.kw}")
            print(f"{index}. {step.step_num} {step.step_name} ... ... ", end="")
            try:
                step_func(step)
                # time.sleep(5)
                print("OK <br />")
            except Exception as e:
                print("Error <br />")
                raise e
