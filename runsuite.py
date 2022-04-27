import unittest
import app
import time
import pymysql
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from scripts.login import login
from scripts.approve import approve
from scripts.trust import trust
from scripts.tender import tender
from scripts.tender_process import Test_Tender_Process


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))
suite.addTest(unittest.makeSuite(approve))
suite.addTest(unittest.makeSuite(trust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(Test_Tender_Process))

report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
with open(report_file,'wb') as f:
    runner = HTMLTestRunner(f, title="P2P金融项目接口测试报告", description="test")
    runner.run(suite)



