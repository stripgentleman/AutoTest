from importlib import import_module

import src.config.actionHandleConfig as Config


class ActionHandlersLoader:
    ac_methods = Config.ac_methods

    @staticmethod
    def load():
        methods_dict = dict()
        ac_methods = ActionHandlersLoader.ac_methods
        for tag in ac_methods:
            if ac_methods.get(tag) is not None:
                method_path = ac_methods[tag].split('.')
                method_module = import_module('.'.join(method_path[:-2]))
                method_object = getattr(method_module, method_path[-2])
                method = getattr(method_object, method_path[-1])
                methods_dict[tag] = method
        return methods_dict


if __name__ == '__main__':
    aa = ActionHandlersLoader.load()

    print(aa)
    aa['test'](32131)

