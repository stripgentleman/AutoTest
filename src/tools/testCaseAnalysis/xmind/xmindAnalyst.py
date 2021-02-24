import zipfile
import json
import os

from src.tools.testCaseAnalysis.abstractAnalyst import AbstractAnalyst


class XmindAnalyst(AbstractAnalyst):

    def analysis(self, case_path, case_name):
        case_path = case_path if case_path[-1] == '\\' or case_path[-1] == '/' else case_path + '/'
        self.unpack_by_zipfile(case_path, case_name)
        case_only_name = ''.join(case_name.split('.')[:-1])
        xmind_dict = self.get_xmind_dicts(case_path, case_only_name)[0]

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


    # def

    # @staticmethod
    # def check_children()->bool:

    @staticmethod
    def goto_final_point(dict_info: dict, list_info: list):
        current_point = dict_info
        current_children = None
        final_point = None
        for point in list_info:
            current_children = current_point.get('children')
            if current_point is None:
                return None
            current_attached = current_children.get('attached')
            if current_point is None:
                return None
            if point in current_attached:
                for children_point in current_attached:
                    if children_point.get('id') == point:
                        current_point = children_point
                    # else:



        return current_point

    @staticmethod
    def import_test():
        print('import success')


if __name__ == '__main__':
    aa = XmindAnalyst()
    aa.analysis('..\\..\\..\\..\\testCase', 'test1.xmind')
