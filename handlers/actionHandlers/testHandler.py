from handlers.abstractHandler import AbstractHandler


class TestHandler(AbstractHandler):

    @staticmethod
    def testmethod(param1,param2,param3):
        print('test111111', param1,param2,param3)


if __name__ == '__main__':
    print('test')