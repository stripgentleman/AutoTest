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
