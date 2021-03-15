#############################################
# 测试用例配置信息
#############################################
#   测试用例存放路径,相对于src/testCaseAnalyst.py的路径或绝对路径
test_case_path = [
    '../testCase',
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
