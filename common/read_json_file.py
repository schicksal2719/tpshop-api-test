import json
from unittest import result


def read_login_json_data(filename):
    with open(filename,"r",encoding="utf-8") as f:
        data_list = json.load(f)
        result = []
        for item in data_list:
            login_data = {
                "username": item["username"],
                "password": item["password"],
                "verify_code": item["verify_code"]
            }
            result.append((
                login_data,
                item["expected_status_code"],
                item["expected_status"],
                item["expected_msg"],
                item["title"]
            ))
        return result

def read_register_json_data(filename):
    with open(filename,"r",encoding="utf-8") as f:
        data_list = json.load(f)
        result = []
        for item in data_list:
            reg_data = {
                "username": item["username"],
                "password": item["password"],
                "password2": item["password2"],
                "verify_code": item["verify_code"]
            }
            result.append((
                reg_data,
                item["expected_status_code"],
                item["expected_status"],
                item["expected_msg"],
                item["title"]
            ))
        return result

def read_add_cart_json_data(filename):
    with open(filename,"r",encoding="utf-8") as f:
        data_list = json.load(f)
        result = []
        for item in data_list:
            cart_data = {
                "goods_id": item["goods_id"],
                "goods_num": item["goods_num"],
            }
            result.append((
                cart_data,
                item.get("need_login", True),
                item["expected_status_code"],
                item["expected_status"],
                item["expected_msg"],
                item["title"]
            ))
        return result

def read_change_num_cart_json_data(filename):
    with open(filename,"r",encoding="utf-8") as f:
        data_list = json.load(f)
        result = []
        for item in data_list:
            cart_data = {
                "cart[id]": item["cart_id"],
                "cart[goods_num]": item["goods_num"],
                "cart[selected]": item["selected"]
            }
            result.append((
                cart_data,
                item["expected_status_code"],
                item["expected_status"],
                item["expected_msg"],
                item["title"]
            ))
        return result

def read_order_json_data(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data_list = json.load(f)
        result = []
        for item in data_list:
            result.append((
                item.get("order_data", {}),
                item.get("need_login", True),
                item.get("need_add_cart", True),
                item.get("need_cart2", True),
                item.get("is_repeat", False),
                item["expected_status_code"],
                item["expected_status"],
                item["expected_msg"],
                item["title"]
            ))
        return result

def read_business_flow_json_data(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data_list = json.load(f)
        result = []
        for item in data_list:
            result.append((
                item.get("login_data", {}),
                item.get("cart_data", {}),
                item.get("change_data", {}),
                item.get("order_data", {}),
                item.get("steps", []),
                item.get("expected_login_status"),
                item.get("expected_cart_status"),
                item.get("expected_change_status"),
                item.get("expected_order_status"),
                item.get("expected_order_msg", ""),
                item.get("expected_order_again_status"),
                item.get("expected_order_again_msg", ""),
                item["title"]
            ))
        return result