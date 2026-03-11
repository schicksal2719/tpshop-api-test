import allure
import requests
import pytest

from api.cart_api import CartApi
from api.login_api import LoginApi
from api.order_api import OrderApi
from common.read_json_file import read_business_flow_json_data
from config import BASE_DIR

# 读取测试数据
business_flow_data = read_business_flow_json_data(BASE_DIR+"/data/business_flow_data.json")


@allure.feature("业务流程")
@allure.story("登录-加购-下单完整流程")
class TestBusinessFlow:
    """完整业务流程测试：登录 → 加购物车 → 确认订单 → 提交订单"""

    def setup_method(self):
        self.session = requests.Session()

    # ==================== 封装每个步骤 ====================
    @allure.step("步骤：登录")
    def step_login(self, login_data, expected_status):
        """步骤：登录"""
        print("\n📌 步骤1：登录")
        LoginApi.get_verify_code(self.session)
        resp = LoginApi.login(self.session, login_data)
        allure.attach(
            str(resp.json()),
            name="登录响应",
            attachment_type=allure.attachment_type.JSON
        )
        if expected_status is not None:
            assert resp.json()["status"] == expected_status
        return resp

    @allure.step("步骤：添加商品到购物车")
    def step_add_cart(self, cart_data, expected_status):
        """步骤：添加商品到购物车"""
        print("\n📌 步骤2：添加商品到购物车")
        resp = CartApi.add_cart(self.session,cart_data)
        allure.attach(
            str(resp.json()),
            name="添加购物车响应",
            attachment_type=allure.attachment_type.JSON
        )
        if expected_status is not None:
            assert resp.json()["status"] == expected_status

        return resp

    @allure.step("步骤：修改购物车数量")
    def step_change_num(self, change_data, expected_status):
        """步骤：修改购物车数量"""
        print("\n📌 步骤3：修改购物车数量")
        resp = CartApi.change_cart(self.session,change_data)
        allure.attach(str(resp.json()), name="修改数量响应", attachment_type=allure.attachment_type.JSON)
        print(f"   修改数量结果：{resp.json()}")
        if expected_status is not None:
            assert resp.json()["status"] == expected_status

        return resp
    @allure.step("步骤：访问购物车页面(cart1)")
    def step_cart1(self):
        """步骤：购物车页面"""
        print("\n📌 步骤4：访问购物车页面(cart1)")
        resp = OrderApi.cart1(self.session)
        print(f"   购物车页面状态码：{resp.status_code}")
        assert resp.status_code == 200
        print("   ✅ 购物车页面访问成功")
        return resp
    @allure.step("步骤：确认订单(cart2)")
    def step_cart2(self):
        """步骤：确认订单页面"""
        print("\n📌 步骤5：确认订单页面(cart2)")
        resp = OrderApi.cart2(self.session)
        print(f"   确认订单页面状态码：{resp.status_code}")
        assert resp.status_code == 200
        print("   ✅ 确认订单页面访问成功")
        return resp

    @allure.step("步骤：提交订单(cart3)")
    def step_cart3(self, order_data, expected_status, expected_msg):
        """步骤：提交订单"""
        print("\n📌 步骤6：提交订单(cart3)")
        resp = OrderApi.cart3(self.session,order_data)
        allure.attach(str(resp.json()), name="提交订单响应", attachment_type=allure.attachment_type.JSON)
        print(f"   提交订单结果：{resp.json()}")
        assert resp.json()["status"] == expected_status
        assert expected_msg in resp.json()["msg"]
        return resp

    @allure.step("步骤：退出登录")
    def step_logout(self):
        """步骤：退出登录"""
        print("\n📌 步骤7：退出登录")
        resp = LoginApi.logout(self.session)
        print(f"   退出状态码：{resp.status_code}")
        assert resp.status_code == 200
        print("   ✅ 退出成功")
        return resp

    # ==================== 参数化测试 ====================

    @pytest.mark.parametrize(
        "login_data, cart_data, change_data, order_data, steps, "
        "expected_login_status, expected_cart_status, expected_change_status, "
        "expected_order_status, expected_order_msg, "
        "expected_order_again_status, expected_order_again_msg, title",
        business_flow_data
    )
    def test_business_flow(self, login_data, cart_data, change_data, order_data,
                           steps, expected_login_status, expected_cart_status,
                           expected_change_status, expected_order_status,
                           expected_order_msg, expected_order_again_status,
                           expected_order_again_msg, title):

        print(f"\n{'='*60}")
        print(f"🔄 业务场景：【{title}】")
        print(f"📋 执行步骤：{steps}")
        print(f"{'='*60}")

        for step in steps:

            if step == "login":
                self.step_login(login_data, expected_login_status)

            elif step == "add_cart":
                self.step_add_cart(cart_data, expected_cart_status)

            elif step == "change_num":
                self.step_change_num(change_data, expected_change_status)

            elif step == "cart1":
                self.step_cart1()

            elif step == "cart2":
                self.step_cart2()

            elif step == "cart3":
                self.step_cart3(order_data, expected_order_status, expected_order_msg)

            elif step == "logout":
                self.step_logout()

            elif step == "cart3_again":
                with allure.step("步骤：退出后再次提交订单"):
                    resp = OrderApi.cart3(self.session, order_data)
                    allure.attach(
                        str(resp.json()),
                        name="再次提交响应",
                        attachment_type=allure.attachment_type.JSON
                    )
                    assert resp.json()["status"] == expected_order_again_status
                    assert expected_order_again_msg in resp.json()["msg"]

        print(f"\n{'='*60}")
        print(f"✅ 【{title}】全部步骤执行完毕！")
        print(f"{'='*60}")