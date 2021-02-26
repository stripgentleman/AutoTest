import zipfile
import json
import os
import ctypes

from src.tools.testCaseAnalysis.abstractAnalyst import AbstractAnalyst


class XmindAnalyst(AbstractAnalyst):

    def analysis(self, case_path, case_name):
        case_path = case_path if case_path[-1] == '\\' or case_path[-1] == '/' else case_path + '/'
        self.unpack_by_zipfile(case_path, case_name)
        case_only_name = ''.join(case_name.split('.')[:-1])
        xmind_dict = self.get_xmind_dicts(case_path, case_only_name)[0]
        # print(str(xmind_dict))
        print(self.get_point_from_str(str(xmind_dict), '657b1f57-2ceb-4fa0-86b6-a94bc9e2669e'))

    @staticmethod
    def unpack_by_zipfile(case_path, case_name, out_put=None):
        zip_case = zipfile.ZipFile(case_path + case_name, mode='r')
        if not out_put:
            try:
                os.mkdir(case_path + ''.join(case_name.split('.')[:-1]))
            except FileExistsError:
                pass
        zip_case.extractall(path=case_path + ''.join(case_name.split('.')[:-1]))

    @staticmethod
    def get_xmind_dicts(case_path, case_only_name):
        with open(case_path + case_only_name + '/content.json', 'r', encoding='utf-8') as json_fp:
            xmind_dicts = json.load(fp=json_fp)
        return xmind_dicts

    @staticmethod
    def method_lists_from_dict(json_dict: dict):
        class_lists = list([])
        root_class = json_dict.get('rootTopic')
        class_stack = list([])
        if root_class is None:
            return None
        if not XmindAnalyst.check_children(root_class):
            return None
        # current_point =

    # def

    @staticmethod
    def check_children(check_dict: dict) -> bool:
        children = check_dict.get('children')
        if isinstance(children, dict):
            return True
        else:
            return False

    @staticmethod
    def load_point(dict_str: str):
        return json.loads(dict_str)

    @staticmethod
    def get_point_from_str(dict_str: str, point_id: str) -> str:
        id_left_index = dict_str.find('\'id\': \'' + point_id)
        if id_left_index == -1:
            return ''
        left_brace_index = id_left_index - 1
        ignore_flag = False
        while (dict_str[left_brace_index] != '{' and left_brace_index >= 0) or ignore_flag:
            if dict_str[left_brace_index] == '\'' and dict_str[left_brace_index - 1] != '\\':
                ignore_flag = not ignore_flag
            left_brace_index -= 1
        if left_brace_index < 0:
            return ''
        right_brace_index = left_brace_index + 1
        ignore_flag = False
        right_flag = 1
        while right_brace_index < len(dict_str):
            if right_flag == 0:
                break
            if dict_str[right_brace_index] == '\'' and dict_str[right_brace_index - 1] != '\\':
                ignore_flag = not ignore_flag
                right_brace_index += 1
                continue
            if ignore_flag:
                right_brace_index += 1
            elif dict_str[right_brace_index] == '{':
                right_flag += 1
                right_brace_index += 1
            elif dict_str[right_brace_index] == '}':
                right_flag -= 1
                right_brace_index += 1
            else:
                right_brace_index += 1

        return dict_str[left_brace_index:right_brace_index]

    @staticmethod
    def get_point_from_children(dict_info: dict, point_id: str):
        children_info = dict_info.get('children')
        if children_info is None:
            return None
        point_str = XmindAnalyst.get_point_from_str(str(children_info), point_id)
        return XmindAnalyst.load_point(point_str)

    @staticmethod
    def import_test():
        print('import success')


if __name__ == '__main__':
    # aa = XmindAnalyst()
    # aa.analysis('..\\..\\..\\..\\testCase', 'test1.xmind')
    class dddd:

        a = 32132112412321321

        def __init__(self):
            self.b = 62142132132532

        @staticmethod
        def static_test():
            print('static')

        @classmethod
        def test(cls):
            print('not static2222222222222222222222222222222222222222222222222222222222')

        def test2(self):
            print('not static1111111111111111111111111111111111111111111')


    aa = dddd()
    a = aa.test2
    c = aa.test2
    b = aa.test
    print(id(a))
    print(id(c))
    print(id(b))
    print(id(c))
    dddd.test()

