import json
import logging
import requests,pymysql
from bs4 import BeautifulSoup

import app


def assert_utils(self, response, status_code, status, desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))


def requests_third_api(form_data):
    # 解析form表单中的内容，并提取第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']  # 获取form标签中action的属性
    logging.info("third request url = {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])  # setdefault(K,V)
    logging.info("third request data = {}".format(data))  # 打印出input标签中所有的name和value
    # 发送第三方请求
    response = requests.post(third_url, data=data)
    logging.info("third request response = {}".format(data))
    return response


class DButils:
    @classmethod
    def get_conn(cls, db_name):
        conn = pymysql.connect(app.DB_URL, app.DB_USERNAME, app.DB_PWD, db_name, autocommit=True)
        return conn

    @classmethod
    def close_conn(cls, cursor=None, conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls, db_name, sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close_conn()


def read_imgVerify_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file, encoding="utf-8") as f:
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"), test_data.get("status_code")))
    print("json data={}".format(test_case_data))
    return test_case_data


def read_register_data(file_name):
    # 注册的测试数据的文件路径
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file, encoding="utf-8") as f:
        # 将json的数据格式转化为字典的数据格式
        register_data = json.load(f)
        # 获取所有数据的列表
        test_case_data_list = register_data.get("test_register")
        # 依次读取测试数据列表中的每一条数据，并进行相应字段的提取
        for test_data in test_case_data_list:
            test_case_data.append((test_data.get("phone"), test_data.get("pwd"), test_data.get("imgVerifyCode"), test_data.get("phoneCode"), test_data.get("dyServer"), test_data.get("invite_phone"), test_data.get("status_code"), test_data.get("status"), test_data.get("description")))
        print("json data = {}".format(test_case_data))
        return test_case_data


# 定义统一的读取所有参数数据文件的方法
def read_param_data(filename, method_name, params_names):
    # filename: 参数数据文件名
    # method_name: 参数数据文件中定义的测试数据列表的名称
    # params_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type，status_code"

    # 获取测试数据文件的文件路径
    file = app.BASE_DIR + "/data/" + filename
    # 获取所有的测试数据的列表
    test_case_data = []
    with open(file,encoding="utf-8") as f:
        # json转字典
        file_data = json.load(f)
        # 获取数据的列表
        test_case_data_list = file_data.get(method_name)
        for test_data in test_case_data_list:
            # 先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in params_names.split(","):
                # 把依次获取每个参数的值添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            # 每完成一组测试数据的读取，就添加到test_case_data_list中，直到所有的测试数据读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data
