import app


class LoginAPI():
    def __init__(self):
        self.getImgCode_url = app.BASE_URL + '/common/public/verifycode1/'
        self.getSmsCode_url = app.BASE_URL + '/member/public/sendSms'
        self.register_url = app.BASE_URL + '/member/public/reg'
        self.login_url = app.BASE_URL + '/member/public/login'

    # 获取图片验证码
    def getImgCode(self, session, r):
        url = self.getImgCode_url + r
        # 发送请求
        response = session.get(url)
        # 返回响应
        return response

    # 获取短信验证码
    def getSmsCode(self, session, phone, imgVerifyCode):
        #准备参数
        data = {'phone': phone, 'imgVerifyCode': imgVerifyCode, 'type': 'reg'}
        #发送请求
        response = session.post(self.getSmsCode_url, data=data)
        #返回响应
        return response

    def register(self, session, phone, pwd, imgVerifyCode= '8888', phoneCode= '666666', dyServer= 'on', invite_phone= ''):
        data = {'phone': phone,
                'password': pwd,
                'verifycode': imgVerifyCode,
                'phone_code': phoneCode,
                'dy_server': dyServer,
                'invite_phone': invite_phone}
        response = session.post(self.register_url, data=data)
        return response

    def login(self, session, phone='1368888888i', pwd='abc123456'):
        data = {"keywords": phone,"password": pwd}
        response = session.post(self.login_url, data=data)
        return response