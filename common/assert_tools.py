def common_login_assert(resp,status_code,status,msg):
    assert status_code == resp.status_code
    assert status == resp.json().get("status")
    assert resp.json().get("msg") in msg

def common_register_assert(resp,status_code,status,msg):
    assert status_code == resp.status_code
    assert status == resp.json().get("status")
    assert resp.json().get("msg") in msg

def common_add_cart_assert(resp,status_code,status,msg):
    assert status_code == resp.status_code
    assert status == resp.json().get("status")
    assert resp.json().get("msg") in msg

def common_order_assert(resp, expected_status_code, expected_status, expected_msg):
    assert resp.status_code == expected_status_code
    assert resp.json()["status"] == expected_status
    assert resp.json()["msg"] in expected_msg