import inspect

from src.tools.handlersLoad.actionHandlersLoaders.actionHandlersLoader import ActionHandlersLoader


class HandlersLoader:

    load_method = dict()

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
    def tag_call_method(tag, args_dict: dict):
        if HandlersLoader.load_method.get(tag) is None:
            HandlersLoader.load_method[tag] = ActionHandlersLoader.load(tag)
        HandlersLoader.method_call(HandlersLoader.load_method[tag], args_dict)


def tes(aaa, bbb):
    print(aaa, bbb)


if __name__ == '__main__':
    # HandlersLoader.method_call(tes, {'aaa': 222, 'bbb':321321})
    HandlersLoader.tag_call_method('test', {'param1':111, 'param2':111, 'param3':111})
    HandlersLoader.tag_call_method('test', {'param1': 151, 'param2': 1771, 'param3': 121})
    HandlersLoader.tag_call_method('test', {'param1': 311, 'param2': 511, 'param3': 131})
    HandlersLoader.tag_call_method('test', {'param3': 111, 'param1': 151, 'param2': 141})
