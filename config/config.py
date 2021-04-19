import os
import logging

base_path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])

##############################
# 用例执行的log相关配置
##############################
running_log_path = base_path + os.path.sep + 'testCase' + os.path.sep + 'testCaseRunningLog.log'
log_enable = True
log_level = logging.DEBUG
log_format = '%(levelname)s - %(asctime)s]: %(message)s'
only_save_last = True

##############################
# 数据库相关配置
##############################
# 数据库类型
database_type = 'sqlite3'
# database_type = 'mysql'
# 数据库连接
conn = 'sqlite3.connect'
# conn = 'pymysql.connect'

