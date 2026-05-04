import requests

BASE_URL = "http://127.0.0.1:5000"

# ========== 1. GET 获取用户列表 ==========
r1 = requests.get(f"{BASE_URL}/api/users")
print("=== 1. 用户列表 ===")
print(f"状态码: {r1.status_code}")
print(f"返回数据: {r1.json()}")
print()

# ========== 2. POST 登录获取Token ==========
login_data = {"username": "admin", "password": "123456"}
r2 = requests.post(f"{BASE_URL}/api/login", json=login_data)
print("=== 2. 登录 ===")
print(f"状态码: {r2.status_code}")
result = r2.json()
print(f"返回数据: {result}")
token = result.get("token")
print(f"提取到的Token: {token}")
print()

# ========== 3. GET 不带Token请求订单（预期失败） ==========
r3 = requests.get(f"{BASE_URL}/api/orders")
print("=== 3. 无Token请求订单 ===")
print(f"状态码: {r3.status_code}")
print(f"返回数据: {r3.json()}")
print()

# ========== 4. GET 带Token请求订单（预期成功） ==========
headers = {"Authorization": f"Bearer {token}"}
r4 = requests.get(f"{BASE_URL}/api/orders", headers=headers)
print("=== 4. 带Token请求订单 ===")
print(f"状态码: {r4.status_code}")
print(f"返回数据: {r4.json()}")
print()

# ========== 5. POST 创建订单 ==========
order_data = {"product_id": 1, "amount": 2}
r5 = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=order_data)
print("=== 5. 创建订单 ===")
print(f"状态码: {r5.status_code}")
print(f"返回数据: {r5.json()}")