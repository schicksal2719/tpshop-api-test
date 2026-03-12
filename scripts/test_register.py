import allure
import pytest
import requests
import time

from api.register_api import RegisterApi
from common.assert_tools import common_register_assert
from common.read_json_file import read_register_json_data
from config import BASE_DIR


reg_list = read_register_json_data(BASE_DIR+"/data/register.json")

@allure.feature("用户模块")
@allure.story("用户注册")
class TestRegister:

    def setup_method(self):
        self.session = requests.Session()
        RegisterApi.get_verify_api(self.session)

    @pytest.mark.parametrize("reg_data,expected_status_code,expected_status,expected_msg,title", reg_list)
    def test_register(self,reg_data,expected_status_code,expected_status,expected_msg,title):
        allure.dynamic.title(title)
        allure.dynamic.description(f"注册用户名：{reg_data['username']}")

        if "成功" in title:
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        else:
            allure.dynamic.severity(allure.severity_level.NORMAL)

        if title == "注册成功":
            timestamp = str(int(time.time()))
            reg_data["username"] = "139" + timestamp[-8:]
            print(f"动态生成手机号：{reg_data['username']}")

        with allure.step("发送注册请求"):
            resp = RegisterApi.register(self.session,reg_data)
            allure.attach(
                str(resp.json()),
                name="注册响应",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step(f"断言：status={expected_status}, msg包含'{expected_msg}'"):
            common_register_assert(resp,expected_status_code,expected_status,expected_msg)
