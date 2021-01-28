import os
import re

from src.config import testCaseConfig


class TestCaseAnalyst:
    postfix_list = testCaseConfig.test_case_postfix
    case_path_list = testCaseConfig.test_case_path
    ignore_case = testCaseConfig.ignore_test_case

    def __init__(self):
        self.type_analyst = {
            '.xmind': 'src.tools.testCaseAnalysis.xmind.xmindAnalyst',
            '.excel': '',
        }

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

    # def


if __name__ == '__main__':
    a = TestCaseAnalyst()
    print(a.get_case_name_dict())
