import zipfile
import json
import os


class XmindAnalyst:

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
    def dfs_class_info(xmind_dict, class_list=None):
        if not class_list:
            class_list = list([])
        if 'children' in xmind_dict:
            class_list.append(xmind_dict['id'])

    @staticmethod
    def import_test():
        print('import success')



if __name__ == '__main__':
    aa = XmindAnalyst()
    aa.analysis('..\\..\\..\\..\\testCase', 'test1.xmind')
