# 测试用例解析器的基础类，包含解析器的基本方法，如果要自定义解析器的话建议继承该类


class AbstractAnalyst:

    @staticmethod
    def json_result2method_lists(json_result: dict):
        pass

    @staticmethod
    def analysis(case_path, case_name):
        pass
