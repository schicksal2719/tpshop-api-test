import requests


class CartApi:
    @staticmethod
    def add_cart(session, cart_data):
        resp =session.post("http://localhost/index.php?m=Home&c=Cart&a=add",data=cart_data)
        return resp

    @classmethod
    def change_cart(cls,session, cart_data):
        resp = session.post(url = "http://localhost/Home/Cart/changeNum.html",data=cart_data)
        return resp

    # ★★★ 新增：删除购物车商品 ★★★
    @staticmethod
    def del_cart(session, cart_id):
        url = "http://localhost/Home/Cart/delete.html"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        data = {"ids": cart_id}
        return session.post(url, data=data, headers=headers)

    # ★★★ 新增：清空购物车 ★★★
    @staticmethod
    def clear_cart(session):
        url = "http://localhost/index.php?m=Home&c=Cart&a=clearCart"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        return session.get(url, headers=headers)