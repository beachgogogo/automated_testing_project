from flask import Flask, jsonify, request

app = Flask(__name__)

# 模拟数据库
users = [
    {"id": 1, "username": "admin", "password": "123456", "role": "admin"},
    {"id": 2, "username": "testuser", "password": "abcdef", "role": "user"}
]

products = [
    {"id": 1, "name": "iPhone 15", "price": 5999, "stock": 100},
    {"id": 2, "name": "MacBook Pro", "price": 14999, "stock": 50}
]

orders = [
    {"id": 101, "user_id": 2, "product_id": 1, "amount": 1, "status": "paid"}
]


@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        # 返回时去掉密码字段（安全）
        safe_user = {k: v for k, v in user.items() if k != 'password'}
        return jsonify(safe_user)
    return jsonify({"error": "User not found"}), 404


@app.route('/api/login', methods=['POST'])
def login():
    """登录，成功后返回Token"""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if user:
        safe_user = {k: v for k, v in user.items() if k != 'password'}
        return jsonify({
            "code": 200,
            "msg": "Login success",
            "token": f"fake_token_{user['id']}",
            "user": safe_user
        })
    return jsonify({"code": 401, "msg": "Invalid username or password"}), 401


@app.route('/api/products', methods=['GET'])
def get_products():
    """获取商品列表"""
    return jsonify(products)


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """获取订单列表（需要认证）"""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    
    return jsonify(orders)


@app.route('/api/orders', methods=['POST'])
def create_order():
    """创建订单（需要认证 + 参数校验）"""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    
    data = request.get_json() or {}
    if 'product_id' not in data or 'amount' not in data:
        return jsonify({"error": "Missing required fields: product_id, amount"}), 400
    
    # 简单校验：amount必须是正整数
    if not isinstance(data['amount'], int) or data['amount'] <= 0:
        return jsonify({"error": "Amount must be a positive integer"}), 400
    
    new_order = {
        "id": len(orders) + 100,
        "user_id": 2,
        "product_id": data['product_id'],
        "amount": data['amount'],
        "status": "created"
    }
    orders.append(new_order)
    return jsonify(new_order), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
