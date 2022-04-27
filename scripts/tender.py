import unittest
import requests
import logging
from utils import requests_third_api
from api.tenderAPI import tenderAPI
from utils import assert_utils
from api.loginAPI import LoginAPI
from api.trustAPI import trustAPI


class tender(unittest.TestCase):
    phone1 = '13688888888'
    tender_id = '56'

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.trust_api = trustAPI()
        self.tender_api = tenderAPI()
        self.session = requests.Session()
        # 登录成功
        response = self.login_api.login(self.session,self.phone1)
        logging.info("login response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

    def tearDown(self) -> None:
        self.session.close()

    def test01_get_loaninfo(self):
        # 获取投资产品详情
        # 请求投资产品的详情
        response = self.tender_api.get_loaninfo(self.session, self.tender_id)
        logging.info("get_loaninfo response = {}".format(response.json()))
        # 断言投资详情是否正确
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual("12", response.json().get("data").get("loan_info").get("id"))

    def test02_tender_success(self):
        # 投资
        # 发送投资请求
        amount = '100'
        response = self.tender_api.tender(self.session,self.tender_id, amount)
        logging.info("tender response = {}".format(response.json()))
        # 断言投资结果是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response = {}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = requests_third_api(form_data)
        logging.info("third_interface response = {}".format(response.text))
        # 断言第三方接口请求是否成功
        self.assertEqual("InitialtiveTender OK", response.text)

    def test03_get_tenderlist(self):
        # 获取我的投资列表
        status = "tender"
        # 发送获取投资列表的请求
        response = self.tender_api.mytender_list(self.session, status)
        logging.info("get_tender_list response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)