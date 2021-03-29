import os
import sys
import re
import logging
import traceback

path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
if path not in sys.path:
    sys.path.append(path)

from src.handlersLoader import HandlersLoader
from src.testCaseAnalyst import TestCaseAnalyst
from src.logService.caseRunLog import CaseRunLog


class Driver:
    def __init__(self):
        self.case_analyst = TestCaseAnalyst()
        self.case_analyst_result = self.case_analyst.analysis()
        self.case_G_param = dict()
        self.logger = CaseRunLog()
        self.log = self.logger.log

    def run_all_handler(self):
        for case_path in self.case_analyst_result:
            self.log(f"begin path {case_path}", logging.INFO)
            self.case_G_param[case_path] = dict()
            for case_name in self.case_analyst_result[case_path]:
                self.log(f"begin testCase {case_path}{os.path.sep}{case_name}", logging.INFO)
                self.case_G_param[case_path][case_name] = dict()
                for handler_call_list in self.case_analyst_result[case_path][case_name]:
                    log_call_chain = list([])
                    for handler_call in handler_call_list:
                        log_call_chain.append(handler_call['description'])
                    self.log(f"begin call chain {str(log_call_chain)}", logging.INFO)
                    for handler_call in handler_call_list:
                        # handler_call like {'tag_type': None, 'tag': None, 'params': None, 'return': None, 'description': '分支主题 1'}
                        if handler_call['tag'] is not None:
                            # print(handler_call['tag'])
                            for param in handler_call['params']:
                                case_g_param_list = re.findall('\${([a-zA-Z_0-9]+)}', handler_call['params'][param])
                                for g_param in case_g_param_list:
                                    if isinstance(self.case_G_param[case_path][case_name][g_param], str):
                                        handler_call['params'][param] = str.replace(handler_call['params'][param], '${' + g_param + '}', self.case_G_param[case_path][case_name][g_param])
                                    else:
                                        handler_call['params'][param] = self.case_G_param[case_path][case_name][g_param]
                            try:
                                self.case_G_param[case_path][case_name][handler_call['return']] = \
                                    HandlersLoader.tag_call_method(handler_call['tag_type'], handler_call['tag'], handler_call['params'])
                                self.log(f"{handler_call['tag_type']} - {handler_call['tag']} run SUCCESS , params:{handler_call['params']}", logging.DEBUG)
                            except Exception as error:
                                self.log(
                                    f"has a ERROR in call chain {str(log_call_chain)}:"
                                    f"\n\t{handler_call['tag_type']} - {handler_call['tag']} , params:{handler_call['params']}, traceback: "
                                    f"\n {traceback.format_exc()}",
                                    logging.ERROR)
                                break
                    self.log(f"finish call chain {str(log_call_chain)}", logging.INFO)
                self.log(f"finish testCase {case_path}{os.path.sep}{case_name}", logging.INFO)
            self.log(f"finish path {case_path}", logging.INFO)


if __name__ == '__main__':
    start = Driver()
    start.run_all_handler()
