import unittest
from typing import Type
from selenium.webdriver.remote.webdriver import WebDriver
import ddt
from src.actions.action import Runner
from src.base.driver_init import get_webdriver
from src.base.models import BaseTestSuite


def create_runner(test_suite: BaseTestSuite):
    return [Runner(case) for case in test_suite.case_list]


def create_tests(test_suite: BaseTestSuite) -> Type[unittest.TestCase]:
    @ddt.ddt
    class Test(unittest.TestCase):
        _test_name = test_suite.name
        driver: WebDriver

        @classmethod
        def setUpClass(cls) -> None:
            cls.driver = get_webdriver("edge")

        @classmethod
        def tearDownClass(cls) -> None:
            cls.driver.quit()

        @ddt.data(*create_runner(test_suite))
        def test(self, runner: Runner):
            runner.run(self)

        def id(self) -> str:
            return "%s.%s" % (self._test_name, self._testMethodName)

        def __str__(self):
            return "%s (%s:%s)" % (
                self._testMethodName,
                "SanmuTestCae",
                self._test_name,
            )

    return Test
