from typing import List, Optional

from pydantic import BaseModel


class TestInfo(BaseModel):
    """用例信息"""
    测试用例编号: str
    测试用例名: str


class TestStep(BaseModel):
    """用例步骤"""

    步骤名: str
    关键字: str
    元素标识: Optional[str]
    元素路径: str
    是否使用参数: bool
    参数: str


class BaseTestCase(BaseModel):
    """测试用例"""

    info: TestInfo
    steps: List[TestStep]


# class BaseTestSuite(BaseModel):
#     """测试套件"""
#     info: TestInfo
#     case_list: List[BaseTestCase]