import os
import sys
import getopt

path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
if path not in sys.path:
    sys.path.append(path)

from src.driver import Driver

driver = Driver()
driver.run_all_handler()
