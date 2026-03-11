import allure
import requests
import pytest

from api.cart_api import CartApi
from api.login_api import LoginApi
from common.assert_tools import common_add_cart_assert
from common.read_json_file import read_change_num_cart_json_data
from config import BASE_DIR

@allure.feature("购物车模块")
@allure.story("修改购物车商品数量")
class TestChangeNumCart:
    @staticmethod
    def do_login(session):
        login_data= {
            "username": "13800138006",
            "password": "123456",
            "verify_code": "8888"
        }
        LoginApi.get_verify_code(session)
        resp = LoginApi.login(session,login_data)

    def setup_method(self):
        self.session = requests.Session()
        self.do_login(self.session)

    cart_data = read_change_num_cart_json_data(BASE_DIR+"/data/cart_changeNum.json")
    @pytest.mark.parametrize("cart_data,expected_status_code,expected_status,expected_msg,title", cart_data)

    def test_change_num_cart(self, cart_data,expected_status_code,expected_status,expected_msg,title):
        """修改的参数"""
        allure.dynamic.title(title)
        allure.dynamic.severity(allure.severity_level.NORMAL)

        with allure.step(f"修改购物车数量：{cart_data}"):
            resp = CartApi.change_cart(self.session, cart_data)
            allure.attach(
                str(resp.json()),
                name="修改数量响应",
                attachment_type=allure.attachment_type.JSON
            )
        with allure.step("断言结果"):
            common_add_cart_assert(resp,expected_status_code,expected_status,expected_msg)