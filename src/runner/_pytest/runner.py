import pytest
from src.base.models import BaseTestSuite
from src.pre_process.extract import parse
from _pytest.python import PyCollector
from _pytest.unittest import UnitTestCase as pytestUnitTestCase, UnitTestCase
from src.runner._unittest.runner import create_tests


class MyPlugin:
    def pytest_collect_file(self, parent, path):
        if path.ext == ".xlsx" and path.basename.startswith("test"):
            return ExcelFile.from_parent(parent, fspath=path)
    def pytest_html_results_table_row(self, report, cells):
        """fix： pytest-html文件名乱码问题"""
        # report.nodeid = report.nodeid.encode("unicode_escape").decode("utf-8")
        if report.fspath.endswith(".xlsx"):
            from py.xml import html
            cells[1] = html.td(report.nodeid, class_="col-name")

class ExcelFile(pytest.File, PyCollector):
    def _getobj(self):
        return self

    def collect(self):
        parser = parse(file=self.fspath)
        for _suite_data in parser.getCaseTest():
            suite = BaseTestSuite(**_suite_data)

            obj = create_tests(suite)
            # yield ExcelItem.from_parent(self, suite=suite, case=case)
            item = UnitTestCase.from_parent(
                self,
                name=suite.name,
                obj=obj,
            )
            yield item


class UnitTestCase(pytestUnitTestCase):
    @classmethod
    def from_parent(cls, parent, *, name, obj=None):
        """The public constructor."""
        s = super().from_parent(name=name, parent=parent)
        s.obj = obj
        return s

# if __name__=='__main__':
#     parser = parse(file="D:\\A\\github.com\\PY\\panda\\src\\test_web.xlsx")
#     for _suite_data in parser.getCaseTest():
#         print("解析后的suit_data")
#         print(_suite_data)
#         suite = BaseTestSuite(**_suite_data)
