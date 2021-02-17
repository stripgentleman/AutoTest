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
            # .后缀名:解析类的包路径.类名.方法名-----------------默认情况下该方法需有且仅有case_path和case_name参数
            '.xmind': 'src.tools.testCaseAnalysis.xmind.xmindAnalyst.XmindAnalyst.analysis',
            '.excel': '',
        }
        self.test_case_dict = self.get_case_name_dict()
        # test_case_dict = {
        #     case_path1:{
        #         case_postfix1:[case_name1,...]
        #         case_postfix2:[case_name1,...]}
        # },
        # ...

    def get_case_name_dict(self):
        test_case_dict = dict()
        for case_path in self.case_path_list:
            test_case_dict[case_path] = dict()
            for postfix in self.postfix_list:
                pattern = re.compile(r'(.*)(' + postfix + ')$')
                test_case_dict[case_path][postfix] = list()
                for case_name in os.listdir(case_path):
                    if case_name in self.ignore_case:
                        continue
                    if pattern.match(case_name):
                        test_case_dict[case_path][postfix].append(case_name)
        return test_case_dict

    def analysis(self):
        for case_path in self.test_case_dict:
            for case_postfix in self.test_case_dict[case_path]:
                if len(self.test_case_dict[case_path][case_postfix]) == 0:
                    continue
                module_path = self.type_analyst[case_postfix].split('.')
                module_name = '.'.join(module_path[:-2])
                analyst_module = import_module(module_name)
                analyst_object = getattr(analyst_module, module_path[-2])
                analyst_method = getattr(analyst_object(), module_path[-1])
                for case_name in self.test_case_dict[case_path][case_postfix]:
                    analysis_result = analyst_method(case_path, case_name)



if __name__ == '__main__':
    a = TestCaseAnalyst()
    print(a.get_case_name_dict())
    a.analysis()