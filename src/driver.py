import os
import sys

path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
if path not in sys.path:
    sys.path.append(path)

from src.handlersLoader import HandlersLoader
from src.testCaseAnalyst import TestCaseAnalyst


class Driver:
    def __init__(self):
        self.case_analyst = TestCaseAnalyst()
        self.case_analyst_result = self.case_analyst.analysis()

    def run_handler(self):
        for handler_step in self.case_analyst_result:
            handler_step
