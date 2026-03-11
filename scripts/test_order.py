import pytest
import requests
import os
import allure

from api.login_api import LoginApi
from api.cart_api import CartApi
from api.order_api import OrderApi
from common.assert_tools import common_order_assert
from common.read_json_file import read_order_json_data
from common.db_helper import DBHelper
from config import BASE_DIR

order_test_data = read_order_json_data(
    os.path.join(BASE_DIR, "data", "order_data.json")
)


@allure.feature("订单模块")
@allure.story("提交订单")
class TestOrder:

    LOGIN_DATA = {
        "username": "13800138006",
        "password": "123456",
        "verify_code": "8888"
    }

    ADD_CART_DATA = {
        "goods_id": "28",
        "goods_num": "1",
        "goods_spec": ""
    }


    @allure.step("前置操作：获取验证码并登录")
    def do_login(self):
        LoginApi.get_verify_code(self.session)
        resp = LoginApi.login(self.session, self.LOGIN_DATA)
        allure.attach(
            str(resp.json()),
            name="登录响应",
            attachment_type=allure.attachment_type.JSON
        )
        assert resp.json()["status"] == 1

    def setup_method(self):
        self.session = requests.Session()
        # ★★★ 每个用例前：数据库清空购物车 ★★★
        DBHelper.clear_cart(user_id=8)

    @allure.step("前置操作：添加商品到购物车")
    def do_add_cart(self):
        resp = CartApi.add_cart(self.session, self.ADD_CART_DATA)
        allure.attach(
            str(resp.json()),
            name="添加购物车响应",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.step("前置操作：访问购物车页面(cart1)")
    def do_cart1(self):
        resp = OrderApi.cart1(self.session)
        allure.attach(str(resp.status_code), name="cart1状态码")
        assert resp.status_code == 200

    @allure.step("前置操作：确认订单(cart2)")
    def do_cart2(self):
        resp = OrderApi.cart2(self.session)
        allure.attach(str(resp.status_code), name="cart2状态码")
        assert resp.status_code == 200

    @pytest.mark.parametrize(
        "order_data, need_login, need_add_cart, need_cart2, is_repeat, "
        "expected_status_code, expected_status, expected_msg, title",
        order_test_data,
        ids=[item[8] for item in order_test_data]
    )
    def test_submit_order(self, order_data, need_login, need_add_cart,
                          need_cart2, is_repeat, expected_status_code,
                          expected_status, expected_msg, title):

        allure.dynamic.title(title)
        allure.dynamic.description(
            f"测试场景：{title}\n"
            f"是否登录：{need_login}\n"
            f"是否加购：{need_add_cart}\n"
            f"是否确认订单：{need_cart2}\n"
            f"是否重复提交：{is_repeat}\n"
            f"订单参数：{order_data}\n"
            f"预期status：{expected_status}\n"
            f"预期msg包含：{expected_msg}"
        )

        if "正常" in title:
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        elif "未登录" in title:
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        elif "重复" in title:
            allure.dynamic.severity(allure.severity_level.CRITICAL)
        else:
            allure.dynamic.severity(allure.severity_level.NORMAL)

        # ===== 第1步：根据需要登录 =====
        if need_login:
            self.do_login()
        else:
            with allure.step("跳过登录：测试未登录场景"):
                allure.attach("不登录，直接操作", name="说明")

        # ===== 第2步：验证购物车已清空 =====
        with allure.step("验证购物车已清空"):
            count = DBHelper.get_cart_count(user_id=8)
            allure.attach(f"购物车商品数量：{count}", name="购物车状态")
            print(f"购物车商品数量：{count}")

        # ===== 第3步：根据需要添加购物车 =====
        if need_add_cart:
            self.do_add_cart()
            self.do_cart1()
        else:
            with allure.step("跳过添加购物车：测试空购物车场景"):
                allure.attach("不添加商品", name="说明")

        # ===== 第4步：根据需要确认订单 =====
        if need_cart2:
            self.do_cart2()
        else:
            with allure.step("跳过确认订单(cart2)"):
                allure.attach("不确认订单，直接提交", name="说明")

        # ===== 第5步：提交订单 =====
        with allure.step("提交订单(cart3)"):
            resp = OrderApi.cart3(self.session, order_data)
            allure.attach(
                str(order_data),
                name="请求参数",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                str(resp.json()),
                name="提交订单响应",
                attachment_type=allure.attachment_type.JSON
            )
            print(f"【{title}】提交订单结果：{resp.json()}")

        # ===== 第6步：重复提交场景 =====
        if is_repeat:
            with allure.step("重复提交订单（第2次）"):
                resp = OrderApi.cart3(self.session, order_data)
                allure.attach(
                    str(resp.json()),
                    name="重复提交响应",
                    attachment_type=allure.attachment_type.JSON
                )
                print(f"【{title}】重复提交结果：{resp.json()}")

        # ===== 第7步：断言 =====
        with allure.step(f"断言：status={expected_status}，msg包含'{expected_msg}'"):
            allure.attach(
                f"预期 status_code = {expected_status_code}\n"
                f"实际 status_code = {resp.status_code}\n"
                f"预期 status = {expected_status}\n"
                f"实际 status = {resp.json()['status']}\n"
                f"预期 msg 包含 = {expected_msg}\n"
                f"实际 msg = {resp.json()['msg']}",
                name="断言对比",
                attachment_type=allure.attachment_type.TEXT
            )
            common_order_assert(resp, expected_status_code, expected_status, expected_msg)