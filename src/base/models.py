from typing import List, Optional

from pydantic import BaseModel


class TestInfo(BaseModel):
    """用例信息"""
    testcase_num: str
    testcase_name: str


class TestStep(BaseModel):
    """用例步骤"""
    step_num: str
    step_name: str
    kw: str
    ele_mark: Optional[str]
    ele_path: str
    param: str
    verify_kw:str
    verify_exp:str



class BaseTestCase(BaseModel):
    """测试用例"""

    info: TestInfo
    steps: List[TestStep]


class BaseTestSuite(BaseModel):
    """测试套件"""
    name: str
    case_list: List[BaseTestCase]
