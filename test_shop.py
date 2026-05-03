import requests

BASE_URL = "http://127.0.0.1:5000"

class TestEcommerceAPI:
    """电商系统接口自动化测试"""
    
    def test_get_users_list(self):
        """测试获取用户列表"""
        r = requests.get(f"{BASE_URL}/api/users")
        # 断言状态码
        assert r.status_code == 200
        # 断言返回是列表
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_user_detail_success(self):
        """测试获取单个用户-存在"""
        r = requests.get(f"{BASE_URL}/api/users/1")
        assert r.status_code == 200
        data = r.json()
        assert data["id"] == 1
        assert "username" in data
        # 安全断言：密码不应该返回
        assert "password" not in data, "安全漏洞：返回了明文密码！"
    
    def test_get_user_detail_not_found(self):
        """测试获取单个用户-不存在（异常场景）"""
        r = requests.get(f"{BASE_URL}/api/users/999")
        assert r.status_code == 404
        assert "error" in r.json()
    
    def test_login_success(self):
        """测试登录成功"""
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(f"{BASE_URL}/api/login", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["code"] == 200
        assert data["msg"] == "Login success"
        assert "token" in data
        assert "password" not in data["user"]
        # 提取token供后续使用（Pytest fixture更优雅，先用简单方式）
        self.token = data["token"]
    
    def test_login_failed_wrong_password(self):
        """测试登录失败-密码错误"""
        payload = {"username": "admin", "password": "wrong_password"}
        r = requests.post(f"{BASE_URL}/api/login", json=payload)
        assert r.status_code == 401
        data = r.json()
        assert data["code"] == 401
        # 安全断言：不应提示"密码错误"或"账号不存在"
        assert "Invalid" in data["msg"]
    
    def test_get_products(self):
        """测试获取商品列表"""
        r = requests.get(f"{BASE_URL}/api/products")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 2
        # 验证商品字段完整性
        for product in data:
            assert all(k in product for k in ["id", "name", "price", "stock"])
    
    def test_get_orders_without_auth(self):
        """测试无Token访问订单-预期401"""
        r = requests.get(f"{BASE_URL}/api/orders")
        assert r.status_code == 401
    
    def test_create_order_success(self):
        """测试创建订单成功"""
        # 先登录获取token
        login_r = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": "admin", "password": "123456"}
        )
        token = login_r.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"product_id": 1, "amount": 2}
        r = requests.post(
            f"{BASE_URL}/api/orders",
            headers=headers,
            json=payload
        )
        assert r.status_code == 201
        data = r.json()
        assert data["product_id"] == 1
        assert data["amount"] == 2
        assert data["status"] == "created"
    
    def test_create_order_invalid_amount(self):
        """测试创建订单-金额非法（异常场景）"""
        login_r = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": "admin", "password": "123456"}
        )
        token = login_r.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        # amount为0，应该失败
        payload = {"product_id": 1, "amount": 0}
        r = requests.post(
            f"{BASE_URL}/api/orders",
            headers=headers,
            json=payload
        )
        assert r.status_code == 400
        assert "error" in r.json()