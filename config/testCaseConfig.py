#############################################
# 测试用例配置信息
#############################################
import os

base_path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
default_path = base_path + os.path.sep + 'testCase'
#   测试用例存放路径,绝对路径
test_case_path = [
    default_path,
]

#   测试用例文件后缀，每种后缀文件的解析方法在src/tools/testCaseAnalyst.py中映射
test_case_postfix = [
    '.xmind',
    '.xlxs',
]

#   忽略的测试用例文件名称
ignore_test_case = [
    '__init__.py'
]

#   测试用例步骤执行完成标志key
run_done = 'task-done'
#   测试用例步骤执行错误标志key
run_wrong = 'symbol-wrong'
