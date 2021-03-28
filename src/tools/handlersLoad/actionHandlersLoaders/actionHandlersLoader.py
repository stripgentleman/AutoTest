from importlib import import_module

import config.actionHandleConfig as Config
from src.tools.handlersLoad import util


class ActionHandlersLoader:
    others_methods_path = Config.ac_methods_path
    ac_methods = Config.ac_methods

    @staticmethod
    def load(tag=None):
        util.insert_methods_path(ActionHandlersLoader.others_methods_path)
        methods_dict = dict()
        ac_methods = ActionHandlersLoader.ac_methods
        if tag is None:
            for temp_tag in ac_methods:
                if ac_methods.get(temp_tag) is not None:
                    methods_dict[temp_tag] = ActionHandlersLoader.load_method(ac_methods[temp_tag])
            return methods_dict
        elif tag not in ac_methods:
            raise SyntaxError(f"ActionHandler {tag} is not in ac_methods, please check config.actionHandleConfig")
        else:
            return ActionHandlersLoader.load_method(ac_methods.get(tag))

    @staticmethod
    def load_method(method_path: str):
        path_list = method_path.split('.')
        method_module = import_module('.'.join(path_list[:-2]))
        method_object = getattr(method_module, path_list[-2])
        method = getattr(method_object, path_list[-1])
        return method


if __name__ == '__main__':
    aa = ActionHandlersLoader.load()

    print(aa)
    # aa['test'](32,13,1)
    #
    # ap = inspect.signature(aa['test'])
    # print(list(ap.parameters))


