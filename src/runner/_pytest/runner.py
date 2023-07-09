from typing import Type
import ddt
from _pytest import unittest

from action import RemoteWebDriver, Runner
from src.base.models import BaseTestSuite
from sanmu.webdriver import get_webdriver
def create_tests(test_suite: BaseTestSuite) -> Type[unittest.TestCase]:
    @ddt.ddt
    class Test(unittest.TestCase):
        _test_name = test_suite.info.name
        driver: RemoteWebDriver

        @classmethod
        def setUpClass(cls) -> None:
            cls.driver = get_webdriver(test_suite.info.browser)

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