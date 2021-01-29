import os
import re
import inspect
from importlib import import_module

from src.config import testCaseConfig


class TestCaseAnalyst:
    postfix_list = testCaseConfig.test_case_postfix
    case_path_list = testCaseConfig.test_case_path
    ignore_case = testCaseConfig.ignore_test_case

    def __init__(self):
        self.type_analyst = {
            # .后缀名:解析类的包路径.类名.方法类
            '.xmind': 'src.tools.testCaseAnalysis.xmind.xmindAnalyst.XmindAnalyst.analysis',
            '.excel': '',
        }
        self.file_dict = self.get_case_name_dict()

    def get_case_name_dict(self):
        file_dict = dict()
        for case_path in self.case_path_list:
            for postfix in self.postfix_list:
                pattern = re.compile(r'(.*)(' + postfix + ')$')
                file_dict[postfix] = list()
                for file_name in os.listdir(case_path):
                    if file_name in self.ignore_case:
                        continue
                    if pattern.match(file_name):
                        file_dict[postfix].append(file_name)
        return file_dict

    def analysis(self):
        for file_postfix in self.file_dict:
            if len(self.file_dict[file_postfix]) == 0:
                continue
            module_path = self.type_analyst[file_postfix].split('.')
            module_name = '.'.join(module_path[:-2])
            analyst_module = import_module(module_name)
            analyst_object = getattr(analyst_module, module_path[-2])
            a = analyst_object()
            analyst_method = getattr(a, module_path[-1])
            analyst_method()


if __name__ == '__main__':
    a = TestCaseAnalyst()
    print(a.get_case_name_dict())
    a.analysis()