import zipfile
import json
import os
import sys
import ctypes

# sys.path.append(os.path.dirname(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.dirname(
#                 os.path.dirname(
#                     os.path.abspath(__file__)))))))
path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-5])
if path not in sys.path:
    sys.path.append(path)

from src.tools.testCaseAnalysis.abstractAnalyst import AbstractAnalyst
from src.tools.testCaseAnalysis.xmind.xmind_list import XmindList


class XmindAnalyst(AbstractAnalyst):
    children_key = 'children'
    summaries_key = 'summaries'
    attached_key = 'attached'
    relationships_key = 'relationships'

    def __init__(self):
        self.global_variable_dict = dict()
        self.id_lists = list([])

    def analysis(self, case_path, case_name):
        case_path = case_path if case_path[-1] == os.path.sep else case_path + os.path.sep
        self.unpack_by_zipfile(case_path, case_name)
        case_only_name = ''.join(case_name.split('.')[:-1])
        xmind_dict = self.get_xmind_dicts(case_path, case_only_name)[0]
        self.id_lists = self.id_lists_from_dict(xmind_dict, case_path, case_name)
        ret_tag_lists = list([])
        for id_list in self.id_lists:
            ret_tag_list = list([])
            for point_id in id_list.to_list():
                point = XmindAnalyst.get_point_from_id(xmind_dict, point_id)
                title = point.get('title', '')

                if title.startswith('{'):
                    right_index = str.find(title, '}')
                    tag_return = str.split(title[1:right_index], ';')
                    params = XmindAnalyst.get_content_dict(point)
                    ret_tag_list.append({'tag_type': tag_return[0], 'tag': tag_return[1], 'params': params, 'return': tag_return[2], 'description': title[right_index + 1:]})
                else:
                    ret_tag_list.append({'tag_type': None, 'tag': None, 'params': None, 'return': None, 'description': title})
            if len(ret_tag_list) > 0:
                ret_tag_lists.append(ret_tag_list)
        return ret_tag_lists

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
        with open(case_path + case_only_name + os.path.sep + 'content.json', 'r', encoding='utf-8') as json_fp:
            xmind_dicts = json.load(fp=json_fp)
        return xmind_dicts

    @staticmethod
    def id_lists_from_dict(json_dict: dict, case_path, case_name):
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
                    if relationship_list[relationship_index][1] in class_list.id_list:
                        loop_point = XmindAnalyst.get_point_from_id(root_class, relationship_list[relationship_index][1])
                        raise SyntaxError(f"has a loop in relationship \"{last_point['title']}\" to \"{loop_point['title']}\" in {case_path}{case_name}")
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
    def get_content_dict(point_dict: dict) -> dict:
        return XmindAnalyst.content_to_dict(XmindAnalyst.get_notes_content(point_dict))

    @staticmethod
    def content_to_dict(content: str) -> dict:
        if len(content) == 0:
            return {}
        content_list = content.split('\n')
        content_dict = dict()
        for content_kv in content_list:
            kv = content_kv.split('=')
            if len(kv) == 2:
                content_dict[kv[0]] = kv[1]
            else:
                raise SyntaxError(content.replace('\n', '\\n') + ': handler params must be \'key=value\' style')
        return content_dict

    @staticmethod
    def get_notes_content(point_dict: dict) -> str:
        notes = point_dict.get('notes')
        if isinstance(notes, dict):
            plain = notes.get('plain')
            if isinstance(plain, dict):
                return plain.get('content', '')
            else:
                return ''
        else:
            return ''

    @staticmethod
    def import_test():
        print('import success')

    @staticmethod
    def print_id_lists(xmind_dict, id_lists):
        for id_list in id_lists:
            temp_list = list([])
            for point_id in id_list.to_list():
                c_point = XmindAnalyst.get_point_from_id(xmind_dict, point_id)
                temp_list.append(c_point.get('title'))
            print(temp_list)


if __name__ == '__main__':
    aa = XmindAnalyst()
    print(aa.analysis('..\\..\\..\\..\\testCase', 'test1.xmind'))
    # aa.content_to_dict('test\n213\ndsa=3')
