#############################################
# 测试handle配置信息
#############################################

default_package_path = 'handlers.actionHandlers.'
action_key = 'AC'

# 非默认路径下的handlers路径列表，使用绝对路径，不用添加后不用拼接到包路径中
ac_methods_path = [

]

ac_methods = {
    # 标志:方法路径
    'test': default_package_path + 'testHandler.TestHandler.testmethod',
    'test2': default_package_path + 'testHandler.TestHandler.testmethod2',
    'test3': default_package_path + 'testHandler.TestHandler.testmethod3',

}
