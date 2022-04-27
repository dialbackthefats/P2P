import unittest
from time import sleep

import requests
import random
import logging
from utils import assert_utils
from api.loginAPI import LoginAPI


class login(unittest.TestCase):
    phone1 = '13688888888'
    phone2 = '13613576785'
    phone3 = '18373994772'
    phone4 = '18373994773'
    phone5 = '18373994774'
    imgCode = '8888'
    phoneCode = '666666'
    pwd = 'abc123456'

    def setUp(self) -> None:
        self.login_api = LoginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 参数为随机小数时，获取图片验证码成功
    def test01_get_imgCode_random_float(self):
        # 定义参数(随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口中的返回结果，进行断言
        self.assertEqual(200, response.status_code)

    # 参数为随机整数时，获取图片验证码成功
    def test02_get_imgCode_random_int(self):
        # 定义参数(随机整数）
        r = random.randint(0, 9999999)
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口中的返回结果，进行断言
        self.assertEqual(200, response.status_code)

    # 参数为空时，获取图片验证码失败
    def test03_get_imgCode_param_is_null(self):
        # 定义参数(参数为空）
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, "")
        # 接收接口中的返回结果，进行断言
        self.assertEqual(404, response.status_code)

    # 参数为随机字母时，获取图片验证码失败
    def test04_get_imgCode_random_str(self):
        # 定义参数(参数为字母）
        r = random.sample("abcdefghijklmnopqrstuvwxyz", 10)    # sample
        rand = ''.join(r)      # 返回的是list，必须对其进行拼接
        print(rand)
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, rand)
        # 接收接口中的返回结果，进行断言
        self.assertEqual(400, response.status_code)

    # 参数正确，获取短信验证码成功
    def test05_get_sms_code_success(self):
        #1、获取图片验证码
        #定义参数(随机小数)
        r = random.random()
        #调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        #接收接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)

        #2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #对收到的响应结果，进行断言
        assert_utils(self,response,200,200, "短信发送成功")

    # 图片验证码错误，获取失败
    def test06_get_PhoneCode_imgCode_wrong(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 图片验证码错误
        error_code = "1234"
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, error_code)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 图片验证码为空，获取失败
    def test07_get_PhoneCode_imgCode_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 图片验证码为空
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, "")
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 手机号码为空，获取失败
    def test08_get_PhoneCode_Phone_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 手机号为空
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, "", self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

    # 未调用图片验证码，获取失败
    def test09_get_PhoneCode_not_imgCode(self):
        # 获取短信验证码
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 输入必填项，注册成功
    def test10_register_success_required_fields(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、输入必填项成功注册
        # 定义参数
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

    # 输入所有项，注册成功
    def test11_register_success_param_all(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 3、输入所有项成功注册
        # 定义参数
        response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone='13688888888')
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

    # 图片验证码错误，注册失败
    def test12_register_fail_imgCode_error(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 图片验证码错误，注册失败
        # 定义参数
        response = self.login_api.register(self.session, self.phone4, self.pwd, '1234')
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误!")

    # 手机号已存在时，注册失败
    def test13_register_fail_phone_exists(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 手机号已存在，注册失败
        # 定义参数
        response = self.login_api.register(self.session, self.phone1, self.pwd,)
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "手机已存在!")

    # 短信验证码错误，注册失败
    def test14_register_fail_phoneCode_error(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 短信验证码错误，注册失败
        # 定义参数
        response = self.login_api.register(self.session, self.phone4, self.pwd, self.imgCode, '555555')
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误")

    # 密码为空，注册失败
    def test15_register_fail_password_is_null(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone3, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 密码为空，注册失败
        # 定义参数
        response = self.login_api.register(self.session, self.phone3,"")
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 未同意协议，注册失败
    def test16_register_fail_disagree_protocol(self):
        # 1、获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)

        # 2、获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")

        # 未同意协议，注册失败
        # 定义参数
        response = self.login_api.register(self.session, self.phone4, self.pwd, self.imgCode, self.phoneCode, 'off')
        logging.info("register response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "请同意我们的条款")

    # 已注册的手机号，登录成功
    def test17_login_success(self):
        # 准备参数
        # 发送请求，调用接口类中的发送登录的请求接口
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

    # 用户名不存在,登录失败
    def test18_login_fail_phone_unexsist(self):
        # 准备参数
        # 发送请求，调用接口类中的发送登录的请求接口
        response = self.login_api.login(self.session, self.phone5, self.pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "用户不存在")

    # 密码为空，登录失败
    def test19_login_fail_pwd_is_null(self):
        # 准备参数
        # 发送请求，调用接口类中的发送登录的请求接口
        response = self.login_api.login(self.session, self.phone1,"")
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 密码错误一次，登录失败
    def test20_login_fail_pwd_error1(self):
        # 准备参数
        error_pwd = 'abc123'
        # 发送请求，调用接口类中的发送登录的请求接口
        response = self.login_api.login(self.session, self.phone1, error_pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        # 密码错误一次，登录失败
        response = self.login_api.login(self.session, self.phone1, error_pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

    # 密码错误三次，登录失败
        response = self.login_api.login(self.session, self.phone1, error_pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

    # 输入正确密码，提示被锁定
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

    # 等待60s，输入正确密码，登录成功
        sleep(60)
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        # 对结果进行断言
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
