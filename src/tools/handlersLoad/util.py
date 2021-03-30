import sys
import logging
from collections import Iterable

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
    def loop(ite):
        def wrapper(method):
            def loop_method(**kwargs):
                if not isinstance(ite, Iterable):
                    raise SyntaxError(f'the loop decorator on {method.__name__} need iterable param, please check it')
                for current_params in ite:
                    HandlerDecorators.caseRunLog(f'handler {method.__name__} is called by loop decorator, params are {current_params}', logging.DEBUG)
                    method(*current_params)
                HandlerDecorators.caseRunLog(f'handler {method.__name__} is called by TeatCase, params are {kwargs}', logging.DEBUG)
                method(**kwargs)
            return loop_method
        return wrapper
