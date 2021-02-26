import inspect

from src.tools.handlersLoad.actionHandlersLoaders.actionHandlersLoader import ActionHandlersLoader
from src.tools.handlersLoad.assertionHandlersLoaders.assertionHandlersLoader import AssertionHandlersLoader


class HandlersLoader:

    ACTION = 'action'
    ASSERTION = 'assertion'

    load_action_method = dict()
    load_assertion_method = dict()

    @staticmethod
    def method_call(fun, arg_dict: dict):
        fun_signature = inspect.signature(fun)
        arg_list = list(fun_signature.parameters)

        args = list()
        for arg in arg_list:
            arg_value = arg_dict.get(arg)
            if arg_value is None:
                arg_value = fun_signature.parameters[arg].default
                if arg_value == inspect.Parameter.empty:
                    error_msg = ''.join([fun.__module__, '.', fun.__name__, '() ', 'get arguments : ', str(arg_dict), ', but missing required positional argument: ', arg])
                    raise TypeError(error_msg)
            args.append(arg_value)
        fun(*args)

    @staticmethod
    def tag_call_method(action_assertion, tag, args_dict: dict):
        if action_assertion == HandlersLoader.ACTION:
            load_method = HandlersLoader.load_action_method
            load = ActionHandlersLoader.load
        elif action_assertion == HandlersLoader.ASSERTION:
            load_method = HandlersLoader.load_assertion_method
            load = AssertionHandlersLoader.load
        else:
            error_msg = ''.join(['HandlersLoader.tag_call_method() get error action_assertion value : ',
                                 action_assertion, ' , it only required \'', HandlersLoader.ACTION, '\' or \'', HandlersLoader.ASSERTION, '\''])
            raise TypeError(error_msg)
        if load_method.get(tag) is None:
            load_method[tag] = load(tag)
        HandlersLoader.method_call(load_method[tag], args_dict)


if __name__ == '__main__':
    # HandlersLoader.method_call(tes, {'aaa': 222, 'bbb':321321})
    HandlersLoader.tag_call_method('action', 'test', {'param1':111, 'param2':111, 'param3':111})
    HandlersLoader.tag_call_method('assertion', 'test', {'param1': 151, 'param2': 1771, 'param3': 121})
    HandlersLoader.tag_call_method('action', 'test2', {'param1': 311, 'param2': 511, 'param3': 131})
    HandlersLoader.tag_call_method('action', 'test', {'param3': 111, 'param1': 151, 'param2': 141})
