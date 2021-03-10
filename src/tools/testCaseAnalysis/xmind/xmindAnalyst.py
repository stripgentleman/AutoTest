import zipfile
import json
import os
import ctypes

from src.tools.testCaseAnalysis.abstractAnalyst import AbstractAnalyst
from src.tools.testCaseAnalysis.xmind.xmind_list import XmindList


class XmindAnalyst(AbstractAnalyst):
    children_key = 'children'
    summaries_key = 'summaries'
    attached_key = 'attached'
    relationships_key = 'relationships'

    def analysis(self, case_path, case_name):
        case_path = case_path if case_path[-1] == '\\' or case_path[-1] == '/' else case_path + '/'
        self.unpack_by_zipfile(case_path, case_name)
        case_only_name = ''.join(case_name.split('.')[:-1])
        xmind_dict = self.get_xmind_dicts(case_path, case_only_name)[0]
        # print(str(xmind_dict))
        # print(self.get_point_from_str(str(xmind_dict), '657b1f57-2ceb-4fa0-86b6-a94bc9e2669e'))
        id_lists = self.id_lists_from_dict(xmind_dict)

        for id_list in id_lists:
            temp_list = list([])
            for point_id in id_list.to_list():
                c_point = XmindAnalyst.get_point_from_id(xmind_dict, point_id)
                temp_list.append(c_point.get('title'))
            print(temp_list)

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
    def id_lists_from_dict(json_dict: dict):
        class_lists = list([])
        root_class = json_dict.get('rootTopic')
        root_list = XmindList()
        if root_class is None:
            return None
        if not XmindAnalyst.check_children(root_class):
            return None
        root_list.append(root_class.get('id'))
        class_lists.append(root_list)
        current_index = 0
        while current_index + 1 <= len(class_lists):
            class_list = class_lists.pop(current_index)
            last_point = XmindAnalyst.get_point_from_id(dict_info=root_class, point_id=class_list.id_list[-1])
            relationship_list = XmindAnalyst.get_relationships_list(json_dict.get(XmindAnalyst.relationships_key))
            relationship_index = 0
            while relationship_index + 1 <= len(relationship_list):
                if relationship_list[relationship_index][0] == last_point['id']:
                    relationship = relationship_list.pop(relationship_index)
                    new_class_list = class_list.build_child(relationship[1])
                    new_class_list.summary_list = list([])
                    class_lists.append(new_class_list)
                else:
                    relationship_index += 1
                    continue

            summaries = last_point.get(XmindAnalyst.summaries_key, list([]))
            children = last_point.get(XmindAnalyst.children_key, {})
            children_attached = children.get(XmindAnalyst.attached_key)
            if children_attached is None:
                if len(class_list.summary_list) > 0:
                    class_list.merge_last_summary()
                    class_lists.insert(current_index, class_list)
                else:
                    class_lists.insert(current_index, class_list)
                    current_index += 1
                continue
            attached_index = 0
            while attached_index + 1 <= len(children_attached):
                new_id = children_attached[attached_index].get('id')
                if new_id is not None:
                    new_class_list = class_list.build_child(new_id)
                    for summary in summaries:
                        range_list = str(summary['range']).replace('(', '').replace(')', '').split(',')
                        if int(range_list[0]) <= attached_index <= int(range_list[1]):
                            new_class_list.append_summary(summary.get('topicId'))
                    class_lists.append(new_class_list)
                    attached_index += 1
        return class_lists

        # def

    @staticmethod
    def get_relationships_list(relationship_list: list):
        ret_relationship_list = list([])
        for relationship in relationship_list:
            ret_relationship_list.append((relationship.get('end1Id'),
                                          relationship.get('end2Id')))
        return ret_relationship_list

    @staticmethod
    def check_children(check_dict: dict) -> bool:
        children = check_dict.get(XmindAnalyst.children_key)
        if isinstance(children, dict):
            return True
        else:
            return False

    @staticmethod
    def load_point(dict_str: str):
        return eval(dict_str)

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
    def get_point_from_id(dict_info: dict, point_id: str):
        point_str = XmindAnalyst.get_point_from_str(str(dict_info), point_id)
        return XmindAnalyst.load_point(point_str)

    @staticmethod
    def import_test():
        print('import success')


if __name__ == '__main__':
    aa = XmindAnalyst()
    aa.analysis('..\\..\\..\\..\\testCase', 'test1.xmind')
