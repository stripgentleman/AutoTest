#############################################
# 断言handle配置信息
#############################################

default_package_path = 'handlers.assertionHandlers.'
assertion_key = 'AS'

# 非默认路径下的handlers路径列表，使用绝对路径，不用添加后不用拼接到包路径中
as_methods_path = [

]
as_methods = {
    # 标志:方法路径
    'test': default_package_path + 'testHandler.TestHandler.testmethod'
}
