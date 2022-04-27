import logging
import random
import unittest
import requests

import app
from api.loginAPI import LoginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI
from utils import assert_utils, DButils
from utils import requests_third_api


class Test_Tender_Process(unittest.TestCase):
    phone1 = '13631866666'
    pwd = 'abc123456'
    tender_id = '56'
    imgVerifyCode = '8888'

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = LoginAPI()
        cls.trust_api = trustAPI()
        cls.tender_api = tenderAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
        sql1 = "delete from mb_member_register_log where phone in " \
               "('13688888888','13613576785','18373994772','18373994773','18373994774');"
        DButils.delete(app.DB_MEMBER, sql1)
        logging.info("delete sql = {}".format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in " \
               "('13688888888','13613576785','18373994772','18373994773','18373994774');"
        DButils.delete(app.DB_MEMBER, sql2)
        logging.info("delete sql = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in " \
               "('13688888888','13613576785','18373994772','18373994773','18373994774');"
        DButils.delete_data(app.DB_MEMBER, sql3)
        logging.info("delete sql = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in " \
               "('13688888888','13613576785','18373994772','18373994773','18373994774');"
        DButils.delete(app.DB_MEMBER, sql4)
        logging.info("delete sql = {}".format(sql4))

    # 注册
    def test01_register_success(self):
        # 请求图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgVerifyCode)
        logging.info("Sms response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

    # 登录
    def test02_login_success(self):
        # 登录成功
        # 发送登录请求
        response = self.login_api.login(self.session, self.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

    # 开户
    def test03_trust_success(self):
        # 1、发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("trust response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 2、发送第三方请求
        form_data = response.json().get("description").get("form")
        logging.info("trust form data response = {}".format(form_data))
        # 调用第三方的请求方法
        response = requests_third_api(form_data)
        logging.info("trust third request response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

    # 充值
    def test04_charge_success(self):
        # 1、发送充值图片验证码
        r = random.random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2、发送充值请求
        response = self.trust_api.recharge(self.session,amount="1000")
        logging.info("charge request response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 3、发送第三方充值请求
        form_data = response.json().get("description").get("form")
        logging.info("charge form data = {}".format(form_data))
        # 调用第三方请求的接口
        response = requests_third_api(form_data)
        logging.info("charge third request response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)

    # 获取投资产品详情
    def test05_loaninfo(self):
        # 请求投资产品的详情
        response = self.tender_api.get_loaninfo(self.session, self.tender_id)
        logging.info("get loaninfo response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual('56', response.json().get("data").get("loan_info").get("id"))

    # 投资
    def test06_tender(self):
        # 发送投资请求
        response = self.tender_api.tender(self.session, self.tender_id, "1000")
        logging.info("tender response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("tender form data response = {}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = requests_third_api(form_data)
        logging.info("tender response = {}".format(response.text))
        self.assertEqual("InitiativeTender OK", response.text)

    # 获取我的投资列表
    def test07_mytender_list(self):
        status = "tender"
        # 发送获取投资列表的请求
        response = self.tender_api.mytender_list(self.session, status)
        logging.info("mytender list response = {}".format(response.json))
        self.assertEqual(200, response.status_code)
