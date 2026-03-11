from http.client import responses

import requests

class LoginApi:
    @classmethod
    def get_verify_code(cls,session):
        session.get(url="http://localhost/index.php?m=Home&c=User&a=verify&r=0.2897559113444156")

    @classmethod
    def login(cls,session,login_data):
        resp = session.post(url="http://localhost/index.php?m=Home&c=User&a=do_login",
                            data=login_data)
        return resp

    @classmethod
    def logout(cls,session):
        resp = session.get("http://localhost/Home/user/logout.html")
        return resp
if __name__ == "__main__":
    session = requests.Session()
    LoginApi.get_verify_code(session)
    login_data = {"username": "13800138006", "password": "123456", "verify_code": "8888"}
    responses = LoginApi.login(session,login_data)
    print("登录结果：", responses.json())
