import allure
import pytest
import requests

from api.login_api import LoginApi

@allure.feature("用户模块")
@allure.story("用户退出")
class TestLogout:

    def setup_method(self):
        """每个用例前：创建session → 获取验证码 → 登录"""
        self.session = requests.Session()
        LoginApi.get_verify_code(self.session)
        login_data = {
            "username": "13800138006",
            "password": "123456",
            "verify_code": "8888"
        }
        resp = LoginApi.login(self.session, login_data)
        print("登录结果：", resp.json())
        # 确认登录成功
        assert resp.json()["status"] == 1

    @allure.title("登录后正常退出")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout_success(self):
        """测试退出成功"""
        # 执行退出
        resp = LoginApi.logout(self.session)
        print("退出结果：", resp.status_code)

        # 断言退出成功（状态码200）
        assert resp.status_code == 200

    def test_visit_after_logout(self):
        """测试退出后无法访问个人中心"""
        # 先退出
        LoginApi.logout(self.session)

        # 再访问个人中心
        url = "http://localhost/Home/User/index.html"
        resp = self.session.get(url)

        # 退出后应该被重定向到登录页（或返回未登录提示）
        print("退出后访问个人中心：", resp.url)
        assert "login" in resp.url.lower() or resp.status_code == 302