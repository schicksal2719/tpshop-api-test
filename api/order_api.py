import requests


class OrderApi:

    """购物车界面"""
    @classmethod
    def cart1(cls,session):
        resp = session.get(url = "http://localhost/Home/Cart/index.html")
        return resp

    """确认订单"""
    @classmethod
    def cart2(cls,session):
        resp = session.get(url = "http://localhost/?m=Home&c=Cart&a=cart2")
        return resp

    @classmethod
    def cart3(cls,session,order_data=None):
        if order_data:
            resp = session.post("http://localhost/?m=Home&c=Cart&a=cart3",data = order_data)
            return resp
        else:
            resp = session.post("http://localhost/?m=Home&c=Cart&a=cart3")
            return resp