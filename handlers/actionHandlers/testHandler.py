from handlers.abstractHandler import AbstractHandler


class TestHandler(AbstractHandler):

    @staticmethod
    def testmethod(param):
        print('test111111', param)


if __name__ == '__main__':
    print('test')