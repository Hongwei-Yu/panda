import logging
import unittest
from typing import Type

import ddt
from src.actions.action import RemoteWebDriver, Runner
from src.base.models import BaseTestSuite
from src.base.driver_init import get_webdriver

logger = logging.getLogger(__name__)


def create_runner(test_suite: BaseTestSuite):
    return [Runner(case) for case in test_suite.case_list]


def create_tests(test_suite: BaseTestSuite) -> Type[unittest.TestCase]:
    @ddt.ddt
    class Test(unittest.TestCase):
        _test_name = test_suite.info.name
        driver: RemoteWebDriver

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
                "TestCae",
                self._test_name,
            )

    return Test
