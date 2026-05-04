import requests
import pytest
import json
import os

# 读取JSON测试数据
DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")
with open(os.path.join(DATA_DIR, "login_cases.json"), encoding="utf-8") as f:
    LOGIN_CASES = json.load(f)

class TestEcommerceAPIV2:
    """电商系统接口自动化测试 - Fixture重构版"""
    
    def test_get_users_list(self, base_url):
        r = requests.get(f"{base_url}/api/users")
        assert r.status_code == 200
        data = r.json()
        assert len(data) >= 2
    
    def test_get_user_success(self, base_url):
        r = requests.get(f"{base_url}/api/users/1")
        assert r.status_code == 200
        assert "password" not in r.json()
    
    def test_get_user_not_found(self, base_url):
        r = requests.get(f"{base_url}/api/users/999")
        assert r.status_code == 404
    
    def test_login_success(self, base_url, auth_token):
        # token已经被fixture验证了，这里只做存在性检查
        assert auth_token.startswith("fake_token_")
    
    def test_login_failed(self, base_url):
        payload = {"username": "admin", "password": "wrong"}
        r = requests.post(f"{base_url}/api/login", json=payload)
        assert r.status_code == 401
    
    def test_get_products(self, base_url):
        r = requests.get(f"{base_url}/api/products")
        assert r.status_code == 200
        assert len(r.json()) == 2
    
    def test_get_orders_no_auth(self, base_url):
        r = requests.get(f"{base_url}/api/orders")
        assert r.status_code == 401
    
    def test_get_orders_with_auth(self, base_url, auth_headers):
        r = requests.get(f"{base_url}/api/orders", headers=auth_headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
    
    def test_create_order_success(self, base_url, auth_headers):
        payload = {"product_id": 1, "amount": 3}
        r = requests.post(f"{base_url}/api/orders", headers=auth_headers, json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["amount"] == 3
        assert data["status"] == "created"
    
    def test_create_order_invalid_amount(self, base_url, auth_headers):
        payload = {"product_id": 1, "amount": -1}
        r = requests.post(f"{base_url}/api/orders", headers=auth_headers, json=payload)
        assert r.status_code == 400

    @pytest.mark.parametrize("case", LOGIN_CASES, ids=lambda x: x["desc"])
    def test_login_parametrize(self, base_url, case):
        """数据驱动：登录多场景"""
        payload = {"username": case["username"], "password": case["password"]}
        r = requests.post(f"{base_url}/api/login", json=payload)
        assert r.status_code == case["expected_status"]