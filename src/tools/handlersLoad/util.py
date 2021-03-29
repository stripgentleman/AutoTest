import sys
import logging
from src.logService.caseRunLog import CaseRunLog


def insert_methods_path(methods_path):
    for path in methods_path:
        if path not in sys.path:
            sys.path.append(path)


class HandlerDecorators:
    caseRunLogger = CaseRunLog()
    caseRunLog = caseRunLogger.log

    @staticmethod
    def skip(method):
        def skip_method(**kwargs):
            HandlerDecorators.caseRunLog(f'handler {method.__name__} is skipped by decorator, params are {kwargs}', logging.INFO)
        return skip_method

    @staticmethod
    def error(method):
        def error_method(**kwargs):
            HandlerDecorators.caseRunLog(f'handler {method.__name__} is error by decorator, params are {kwargs}', logging.ERROR)
        return error_method

    @staticmethod
    def loop(method, times:int, ite):
        def loop_method(**kwargs):

            for current_param in ite:
                HandlerDecorators.caseRunLog(f'handler {method.__name__} is looping by decorator, params are {current_param}', logging.DEBUG)


