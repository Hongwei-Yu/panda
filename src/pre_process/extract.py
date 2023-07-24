import pandas as pd
import numpy as np


class parse:
    def __init__(self, filetype='excel', file='./TestCase'):
        self._filetype = filetype
        self._file = file

    def getCaseTest(self):
        excel = pd.read_excel(self._file, sheet_name=None)

        for sheet in excel:
            print("这里是sheet\t" + sheet)
            yield self.parseSheet(sheet=excel[sheet],sheetName=sheet)

    def parseSheet(self, sheet=None, file=None,sheetName=None):
        if file is None:
            file = self._file
        if sheet is None:
            sheet = pd.read_excel(file)
        # print(sheet.keys())
        if sheetName is None:
            sheetName = "Testsuit"
        stop = 0
        caseList = []
        步骤集 = []
        length = len(sheet)
        for row in sheet.iterrows():
            if np.isnan(row[1]['测试用例编号']) == False and stop == 0:
                if row[0] != 0:
                    caseList.append(self.copyCase(测试用例编号, 测试用例名, 步骤集))
                    步骤集 = []
                测试用例编号 = row[1]['测试用例编号']
                测试用例名 = row[1]['测试用例名']
                步骤集.append(self.copyrow(row[1]))
                stop = 1
            else:
                stop = 0
                步骤集.append(self.copyrow(row[1]))
                if row[0] + 1 == length:
                    caseList.append(self.copyCase(测试用例编号, 测试用例名, 步骤集))
        return {'name': sheetName, 'case_list': caseList}

    def copyrow(self, row):
        步骤 = {'step_num': str(row['步骤序号']), 'step_name': str(row['步骤名']), 'kw': str(row['关键字']),
                'ele_mark': str(row['元素标识']), 'ele_path': str(row['元素路径']), 'param': str(row['参数']),
                'verify_kw': str(row['验证关键字']), 'verify_exp': str(row['验证表达式'])}
        return 步骤

    def copyCase(self, 测试用例编号, 测试用例名, 步骤集):
        newCase = {'info': {'testcase_num': str(测试用例编号), 'testcase_name': 测试用例名}, 'steps': 步骤集}
        return newCase
