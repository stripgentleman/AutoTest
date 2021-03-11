from handlers.abstractHandler import AbstractHandler
from handlers.actionHandlers.paramtest import asd


class TestHandler(AbstractHandler):
    aa = dict()
    aa['dsa'] = 'e'
    print('load module')
    print(id(asd))

    @staticmethod
    def testmethod(param1, param2, param3):
        print('test111111', param1, param2, param3)


    @staticmethod
    def testmethod2(param1, param2, param3):
        print('test111111', param1, param2, param3)


    @staticmethod
    def testmethod3(a,b=1,**kwargs):
        print(a,b,kwargs)

if __name__ == '__main__':
    print('test')
