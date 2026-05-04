import requests
import pytest
import allure
import json
import os

BASE_URL = "http://127.0.0.1:5000"
DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")
with open(os.path.join(DATA_DIR, "login_cases.json"), encoding="utf-8") as f:
    LOGIN_CASES = json.load(f)


@allure.feature("用户模块")
class TestUserModule:
    """用户相关接口测试"""
    
    @allure.story("获取用户列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_users_list(self):
        r = requests.get(f"{BASE_URL}/api/users")
        with allure.step("验证状态码为200"):
            assert r.status_code == 200
        with allure.step("验证返回是列表且长度≥2"):
            data = r.json()
            assert len(data) >= 2
        allure.attach(str(data), "响应数据", allure.attachment_type.JSON)
    
    @allure.story("获取单个用户详情")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_success(self):
        r = requests.get(f"{BASE_URL}/api/users/1")
        with allure.step("验证状态码200"):
            assert r.status_code == 200
        with allure.step("验证不返回明文密码（安全校验）"):
            data = r.json()
            assert "password" not in data, "安全漏洞：响应中包含password字段"
        allure.attach(str(data), "响应数据", allure.attachment_type.JSON)
    
    @allure.story("获取不存在的用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_not_found(self):
        r = requests.get(f"{BASE_URL}/api/users/999")
        with allure.step("验证返回404"):
            assert r.status_code == 404


@allure.feature("登录认证模块")
class TestLoginModule:
    """登录相关接口测试"""
    
    @allure.story("登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self):
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(f"{BASE_URL}/api/login", json=payload)
        with allure.step("发送登录请求"):
            pass
        with allure.step("验证状态码200"):
            assert r.status_code == 200
        with allure.step("验证响应包含token"):
            data = r.json()
            assert "token" in data
            allure.attach(data["token"], "提取的Token", allure.attachment_type.TEXT)
    
    @allure.story("登录失败-密码错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_failed(self):
        payload = {"username": "admin", "password": "wrong"}
        r = requests.post(f"{BASE_URL}/api/login", json=payload)
        with allure.step("验证返回401"):
            assert r.status_code == 401
    
    @allure.story("登录多场景数据驱动")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", LOGIN_CASES, ids=lambda x: x["desc"])
    def test_login_parametrize(self, case):
        allure.dynamic.title(f"登录场景：{case['desc']}")
        with allure.step(f"输入账号：{case['username']}，密码：{case['password']}"):
            payload = {"username": case["username"], "password": case["password"]}
            r = requests.post(f"{BASE_URL}/api/login", json=payload)
        with allure.step(f"验证状态码为 {case['expected_status']}"):
            assert r.status_code == case["expected_status"]


@allure.feature("商品模块")
class TestProductModule:
    """商品相关接口测试"""
    
    @allure.story("获取商品列表")
    def test_get_products(self):
        r = requests.get(f"{BASE_URL}/api/products")
        assert r.status_code == 200
        assert len(r.json()) == 2


@allure.feature("订单模块")
class TestOrderModule:
    """订单相关接口测试"""
    
    token = None
    
    def setup_method(self):
        """每个订单测试前自动登录"""
        r = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": "admin", "password": "123456"}
        )
        self.token = r.json()["token"]
    
    @allure.story("无Token访问订单-鉴权失败")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_no_auth(self):
        r = requests.get(f"{BASE_URL}/api/orders")
        with allure.step("验证返回401"):
            assert r.status_code == 401
    
    @allure.story("正确Token访问订单列表")
    def test_get_orders_with_auth(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{BASE_URL}/api/orders", headers=headers)
        with allure.step("验证状态码200"):
            assert r.status_code == 200
        with allure.step("验证返回是列表"):
            assert isinstance(r.json(), list)
    
    @allure.story("创建订单成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_order_success(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"product_id": 1, "amount": 3}
        with allure.step("发送创建订单请求"):
            r = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=payload)
        with allure.step("验证状态码201"):
            assert r.status_code == 201
        with allure.step("验证金额和状态正确"):
            data = r.json()
            assert data["amount"] == 3
            assert data["status"] == "created"
            allure.attach(str(data), "创建的订单数据", allure.attachment_type.JSON)
    
    @allure.story("创建订单-非法金额")
    def test_create_order_invalid_amount(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"product_id": 1, "amount": -1}
        r = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=payload)
        assert r.status_code == 400