import pytest

from src.base.models import BaseTestSuite
from src.pre_process.extract import parse

from _pytest.python import PyCollector
from _pytest.unittest import UnitTestCase as pytestUnitTestCase

class ExcelFile(pytest.File, PyCollector):
    def _getobj(self):
        return self

    def collect(self):
        for _suite_data in parse.parseSheet(self.fspath):
            suite = BaseTestSuite(**_suite_data)

            obj = create_tests(suite)
            # yield ExcelItem.from_parent(self, suite=suite, case=case)
            item = UnitTestCase.from_parent(
                self,
                name=suite.info.name,
                obj=obj,
            )
            yield item