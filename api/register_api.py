
class RegisterApi:
    @classmethod
    def get_verify_api(cls,session):
        session.get(url="http://localhost/index.php?m=Home&c=User&a=verify&r=0.2897559113444156")

    @classmethod
    def register(cls,session,reg_data):
        resp = session.post(url = "http://localhost/Home/User/reg.html",data =reg_data)
        return resp