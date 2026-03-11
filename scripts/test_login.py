import allure
import pytest
import requests

from api.login_api import LoginApi
from common.assert_tools import common_login_assert
from common.read_json_file import read_login_json_data
from config import BASE_DIR

login_test_data =read_login_json_data(BASE_DIR+"/data/login_data.json")



@allure.feature("用户模块")
@allure.story("用户登录")
class TestLogin:
    def setup_method(self):
        self.session = requests.Session()
        LoginApi.get_verify_code(self.session)

    @pytest.mark.parametrize("login_data, expected_status_code, expected_status, expected_msg, title", login_test_data)
    def test_login(self,login_data, expected_status_code, expected_status, expected_msg, title):

        allure.dynamic.title(title)
        allure.dynamic.description(f"用户名：{login_data.get('username')}")

        with allure.step("发送登录请求"):
            resp = LoginApi.login(self.session, login_data)
            allure.attach(
                str(resp.json()),
                name = "登陆响应",
                attachment_type = allure.attachment_type.JSON
            )

        with allure.step(f"断言：status={expected_status}, msg包含'{expected_msg}'"):
            common_login_assert(resp,expected_status_code,expected_status,expected_msg)

