import allure
import requests
import pytest

from api.cart_api import CartApi
from api.login_api import LoginApi
from common.assert_tools import common_add_cart_assert
from common.read_json_file import read_add_cart_json_data
from config import BASE_DIR

@allure.feature("购物车模块")
@allure.story("添加商品到购物车")
class TestAddCart:
    def do_login(self,session):
        login_data = {
            "username": "13800138006",
            "password": "123456",
            "verify_code": "8888"
        }
        LoginApi.get_verify_code(session)
        resp = LoginApi.login(self.session,login_data)
        assert resp.json()["status"] == 1

    def setup_method(self):
        """创建session对象"""
        self.session = requests.Session()

    add_cart_data = read_add_cart_json_data(BASE_DIR+"/data/add_cart.json")
    @pytest.mark.parametrize("cart_data,need_login,expected_status_code,expected_status,expected_msg,title", add_cart_data)

    def test_add_cart(self, cart_data,need_login,expected_status_code,expected_status,expected_msg,title):
        """判断是否需要登录"""
        allure.dynamic.title(title)

        if "正常" in title:
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        elif title in self.KNOWN_BUGS:
            allure.dynamic.severity(allure.severity_level.MINOR)
        else:
            allure.dynamic.severity(allure.severity_level.NORMAL)

        if need_login:
            with allure.step("前置：登录"):
                self.do_login(self.session)
        """执行添加购物车"""
        with allure.step("添加商品到购物车"):
            resp = CartApi.add_cart(self.session,cart_data)
            allure.attach(
                str(resp.json()),
                name="添加购物车响应",
                attachment_type=allure.attachment_type.JSON
            )

        """断言"""
        with allure.step("断言结果"):
            common_add_cart_assert(resp, expected_status_code, expected_status, expected_msg)

        if title in self.KNOWN_BUGS:
            if resp.json()["status"] == 1:
                allure.attach(
                    f"【{title}】应返回失败，但返回了成功",
                    name="⚠️ BUG",
                    attachment_type=allure.attachment_type.TEXT
                )