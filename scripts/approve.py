import logging
import unittest
import requests
from api.approveAPI import approveAPI
from api.loginAPI import LoginAPI
from utils import assert_utils


class approve(unittest.TestCase):
    phone1 = '13688888888'
    phone2 = '13613576785'
    realname = '张三'
    cardId = '440711123443211234'

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 认证成功
    def test01_approve_success(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、认证
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, self.realname, self.cardId)
        logging.info("approve response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "提交成功!")

    # 姓名为空，认证失败
    def test02_approve_fail_name_is_null(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone2)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、认证
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, "", self.cardId)
        logging.info("approve response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "姓名不能为空")

    # 身份证为空，认证失败
    def test03_approve_fail_id_is_null(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone2)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、认证
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, self.realname, "")
        logging.info("approve response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "身份证号不能为空")

    # 获取认证信息
    def test04_getapprove(self):
        # 1、用户登录
        response = self.login_api.login(self.session, self.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、获取认证信息
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.get_approve(self.session)
        logging.info("approve response = {}".format(response.json()))
        # 对结果进行断言
        self.assertEqual(200, response.status_code)