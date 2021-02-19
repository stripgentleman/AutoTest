import inspect


class HandlersLoader:

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
                    raise TypeError(fun.__name__ + '() missing 1 required positional argument: ' + arg)
            args.append(arg_value)
        fun(*args)


def tes(aaa, bbb):
    print(aaa, bbb)


if __name__ == '__main__':
    HandlersLoader.method_call(tes, {'aaa': 222, 'bbb':321321})