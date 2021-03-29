from handlers.abstractHandler import AbstractHandler
from handlers.actionHandlers.paramtest import asd
from src.tools.handlersLoad.util import HandlerDecorators


class TestHandler(AbstractHandler):
    # aa = dict()
    # aa['dsa'] = 'e'
    # print('load module')
    # print(id(asd))

    @staticmethod
    def testmethod(param1, param2, param3):
        print('test111111', param1, param2, param3)
        return 'testreturn'


    @staticmethod
    @HandlerDecorators.error
    def testmethod2(param1, param2, param3):
        print('test2222', param1, param2, param3)


    @staticmethod
    def testmethod3(a,b=1,**kwargs):
        print(a,b,kwargs)

if __name__ == '__main__':
    print('test')
