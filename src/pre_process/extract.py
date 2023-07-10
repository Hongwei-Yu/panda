import pandas as pd
import numpy as np
from src.base.models import *

class parse:
    def __init__(self, filetype='excel', file='./TestCase'):
        self._filetype = filetype
        self._file = file

    def getCaseTest(self):
        excel = pd.read_excel(self._file)

        for sheet in excel:
            self.parseSheet(sheet)


    def parseSheet(self,sheet=None,file=None):
        if file is None:
            file = self._file
        if sheet is None:
            sheet = pd.read_excel(file)
        print(sheet.keys())
        stop = 0
        caseList = []
        步骤集 = []
        length = len(sheet)
        for row in sheet.iterrows():
            if np.isnan(row[1]['测试用例编号']) == False and stop == 0:
                if row[0] != 0:
                    caseList.append(self.copyCase(测试用例编号, 测试用例名,步骤集))
                    步骤集 = []
                测试用例编号 = row[1]['测试用例编号']
                测试用例名 = row[1]['测试用例名']
                步骤集.append(self.copyrow(row[1]))
                stop = 1
            else:
                stop = 0
                步骤集.append(self.copyrow(row[1]))
                if row[0]+1 == length:
                    caseList.append(self.copyCase(测试用例编号, 测试用例名, 步骤集))
        return {'name':'testsuit','case_list':caseList}

    def copyrow(self,row):
        步骤 = {'步骤序号': str(row['步骤序号']), '步骤名': str(row['步骤名']), '关键字': str(row['关键字']),
                '元素标识': str(row['元素标识']), '元素路径': str(row['元素路径']), '参数': str(row['参数'])}
        return 步骤

    def copyCase(self,测试用例编号, 测试用例名, 步骤集):
        newCase = {'info':{'测试用例编号': str(测试用例编号), '测试用例名': 测试用例名}, '步骤': 步骤集}
        return newCase

if __name__ == '__main__':
    parser = parse(file = "E:\github.com\python_project\工作簿1.xlsx")
    a = parser.parseSheet(None)
    print(a)
    suit = BaseTestSuite(**a)
    print(suit)