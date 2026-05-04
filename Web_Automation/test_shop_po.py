# test_shop_po.py
import pytest
import allure
from shop_api_client import APIClient

@pytest.fixture
def client():
    c = APIClient("http://127.0.0.1:5000")
    c.login("admin", "123456")  # 前置登录
    return c

@pytest.fixture
def visitor():
    v = APIClient("http://127.0.0.1:5000")
    return v

@allure.feature("shop_test-PageObject版")
class TestWithClient:

    @allure.story("获取用户列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_users_list(self, visitor):
        r = visitor.get_user_list()
        with allure.step("验证状态码为200"):
            assert r.status_code == 200
        with allure.step("验证返回是列表且长度≥2"):
            data = r.json()
            assert len(data) >= 2

    @allure.story("获取不存在的用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_not_found(self, visitor):
        r = visitor.get_user(999)
        with allure.step("验证状态码为404"):
            assert r.status_code == 404

    @allure.story("正确Token访问订单列表")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_orders(self, client):
        r = client.get_orders()
        with allure.step("验证状态码为200"):
            assert r.status_code == 200

    @allure.story("不带Token访问订单列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_no_auth(self, visitor):
        r = visitor.get_orders_no_auth()
        with allure.step("验证状态码为401"):
            assert r.status_code == 401
    
    @allure.story("创建订单成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_order(self, client):
        r = client.create_order(1, 5)
        with allure.step("验证状态码为201"):
            assert r.status_code == 201
        with allure.step("验证返回订单个数是否为5"):
            assert r.json()["amount"] == 5

    @allure.story("访问产品内容")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_orders_no_auth(self, visitor):
        r = visitor.get_product_no_auth()
        with allure.step("验证状态码为200"):
            assert r.status_code == 200