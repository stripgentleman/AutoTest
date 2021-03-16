from importlib import import_module

import config.assertionHandleConfig as Config

class AssertionHandlersLoader:
    as_methods = Config.as_methods

    @staticmethod
    def load(tag=None):
        methods_dict = dict()
        as_methods = AssertionHandlersLoader.as_methods
        if tag is None:
            for temp_tag in as_methods:
                if as_methods.get(temp_tag) is not None:
                    methods_dict[temp_tag] = AssertionHandlersLoader.load_method(as_methods[temp_tag])
            return methods_dict
        elif tag not in as_methods:
            raise SyntaxError(f"AssertionHandler {tag} is not in as_methods, please check config.assertionHandleConfig")
        else:
            return AssertionHandlersLoader.load_method(as_methods.get(tag))

    @staticmethod
    def load_method(method_path: str):
        path_list = method_path.split('.')
        method_module = import_module('.'.join(path_list[:-2]))
        method_object = getattr(method_module, path_list[-2])
        method = getattr(method_object, path_list[-1])
        return method

