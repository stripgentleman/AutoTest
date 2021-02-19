from importlib import import_module

import src.config.assertionHandleConfig as Config

class AssertionHandlersLoader:
    as_method = Config.as_method

    @staticmethod
    def load(tag=None):
        methods_dict = dict()
        as_method = AssertionHandlersLoader.as_method
        if tag is None:
            for temp_tag in as_method:
                if as_method.get(temp_tag) is not None:
                    methods_dict[temp_tag] = AssertionHandlersLoader.load_method(as_method[temp_tag])
            return methods_dict
        else:
            return AssertionHandlersLoader.load_method(as_method.get(tag))

    @staticmethod
    def load_method(method_path: str):
        path_list = method_path.split('.')
        method_module = import_module('.'.join(path_list[:-2]))
        method_object = getattr(method_module, path_list[-2])
        method = getattr(method_object, path_list[-1])
        return method

