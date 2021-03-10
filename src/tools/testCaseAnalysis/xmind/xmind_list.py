from src.tools.testCaseAnalysis.abstractList import AbstractList


class XmindList(AbstractList):
    def __init__(self, summary_list: list = None, id_list: list = None):
        self.summary_list = list([]) if summary_list is None else summary_list.copy()

        self.id_list = list([]) if id_list is None else id_list.copy()

    def copy(self):
        return XmindList(summary_list=self.summary_list, id_list=self.id_list)

    def append(self, point_id: str):
        self.id_list.append(point_id)

    def append_summary(self, point_id: str):
        self.summary_list.append(point_id)

    def build_child(self, child_id: str):
        new_child_list = XmindList(self.summary_list, self.id_list)
        new_child_list.append(child_id)
        return new_child_list

    def to_list(self) -> list:
        ret_list = self.id_list.copy()
        temp_summary_list = self.summary_list.copy()
        temp_summary_list.reverse()
        ret_list.extend(temp_summary_list)
        del temp_summary_list
        return ret_list

    def merge_last_summary(self):
        self.id_list.append(self.summary_list.pop())

if __name__ == '__main__':
    al = list([1, 2, 3, 4])
    aal = list([5, 6, 7, 8])
    a = XmindList(al, aal)
    b = XmindList(al, aal)
    a.append('321321')
    print(id(a.summary_list))
    print(id(b.summary_list))
    print(id(a.id_list))
    print(id(b.id_list))
    print(a.summary_list)
    print(b.summary_list)
    print(a.id_list)
    print(b.id_list)
    print(a.to_list(), a.summary_list)
