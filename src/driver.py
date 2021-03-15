import os
import sys
import re

path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
if path not in sys.path:
    sys.path.append(path)

from src.handlersLoader import HandlersLoader
from src.testCaseAnalyst import TestCaseAnalyst


class Driver:
    def __init__(self):
        self.case_analyst = TestCaseAnalyst()
        self.case_analyst_result = self.case_analyst.analysis()
        self.case_G_param = dict()

    def run_all_handler(self):
        for case_path in self.case_analyst_result:
            self.case_G_param[case_path] = dict()
            for case_name in self.case_analyst_result[case_path]:
                self.case_G_param[case_path][case_name] = dict()
                for handler_call_list in self.case_analyst_result[case_path][case_name]:
                    for handler_call in handler_call_list:
                        # handler_call like {'tag_type': None, 'tag': None, 'params': None, 'return': None, 'description': '分支主题 1'}
                        if handler_call['tag'] is not None:
                            # print(handler_call['tag'])
                            for param in handler_call['params']:
                                case_g_param_list = re.findall('\${([a-zA-Z_0-9]+)}', handler_call['params'][param])
                                for g_param in case_g_param_list:
                                    if isinstance(self.case_G_param[case_path][case_name][g_param], str):
                                        handler_call['params'][param] = str.replace(handler_call['params'][param], '${' + g_param + '}', self.case_G_param[case_path][case_name][g_param])

                            self.case_G_param[case_path][case_name][handler_call['return']] = \
                                HandlersLoader.tag_call_method(handler_call['tag_type'], handler_call['tag'], handler_call['params'])


if __name__ == '__main__':
    start = Driver()
    start.run_all_handler()
    # aa = re.findall('\${([a-zA-Z_0-9]+)}', 'fsadsa${dsadsadsa}fdfa')
    # print(aa)
