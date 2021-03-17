# AutoTest
 用于自动化执行测试用例
##推荐用法(以xmind为例)
1. 首先编写测试用例执行时用到的动作单元或断言函数，放入handlers/actionHandlers/或handlers/assertionHandlers/中。
2. 在config/actionHandleConfig.ac_methods和config/assertionHandleConfig.as_methods中注册编写的handler及其tag。
3. 在xmind中编写测试用例，调用handle的格式如下，注：使用英文分号;进行分隔，要把{}放最前面

   {AC;tag名;参数}主题描述 解释如下：
   
   AC：handler类型，默认类型有AC、AS，在actionHandleConfig.action_key和assertionHandleConfig.assertion_key设
   
   tag名：config/actionHandleConfig.ac_methods和config/assertionHandleConfig.as_methods中注册的tag名
   
   参数：执行handler的参数使用key=value的形式
   
   主题描述：对该主题的描述，对执行无影响，用例说明
 
 内置xmind测试用例解析器，可把xmind文件解析为函数调用链并自动执行。
