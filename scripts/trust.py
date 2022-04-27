import random
import unittest
import logging
import requests
from bs4 import BeautifulSoup
from utils import assert_utils, requests_third_api
from api.loginAPI import LoginAPI
from api.trustAPI import trustAPI


class trust(unittest.TestCase):
    phone1 = '13688888888'

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.trust_api = trustAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 开户请求
    def test01_trust_success(self):
        # 1、认证通过的账号登录
        response = self.login_api.login(self.session,self.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("login response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 3、发送第三方的开户请求
        form_data = response.json().get("description").get("form")
        logging.info("form response = {}".format(form_data))
        # 调用第三方接口的请求方法
        response = requests_third_api(form_data)
        # 封装下面的代码

        # # 解析form表单中的内容，并提取第三方请求的参数
        # soup = BeautifulSoup(form_data,"html.parser")
        # third_url = soup.form['action']
        # logging.info("third request url = {}".format(third_url))
        # data = {}
        # for input in soup.find_all('input'):
        #     data.setdefault(input['name'], input['value'])
        # logging.info("third request data = {}".format(data))
        # # 发送第三方请求
        # response = requests.post(third_url,data=data)

        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    # 充值成功
    def test02_recharge_success(self):
        # 1、登录成功
        response = self.login_api.login(self.session, self.phone1)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、获取充值验证码
        r = random.random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        logging.info("get recharge verify code response = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        # 3、发送充值请求
        response = self.trust_api.recharge(self.session, "10000")
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 4、发送第三方充值请求
        # 获取响应中form表单的数据，并提取为第三方请求的数据
        form_data = response.json().get("description").get("form")
        logging.info("form response = {}".format(form_data))
        # 调用第三方请求的接口
        response = requests_third_api(form_data)
        logging.info("requests_third charge response = {}".format(response.text))
        # 断言
        self.assertEqual('NetSave OK', response.text)