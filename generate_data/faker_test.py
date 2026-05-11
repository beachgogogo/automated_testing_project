from faker import Faker
import json
import random

fake = Faker('zh_CN')

def generate_users(count=100):
    """生成测试用户数据"""
    users = []
    roles = ['admin', 'user', 'guest']
    
    for i in range(count):
        user = {
            "id": i + 1,
            "username": fake.user_name() + str(i),  # 加序号避免重复
            "password": fake.password(length=8),
            "role": random.choice(roles),
            "phone": fake.phone_number(),
            "email": fake.email(),
            "created_at": fake.date_time_this_year().isoformat()
        }
        users.append(user)
    return users

def generate_products(count=20):
    """生成测试商品数据"""
    products = []
    product_names = [
        "iPhone 15 Pro", "MacBook Air M3", "AirPods Pro 2",
        "iPad Air", "小米14 Ultra", "华为Mate 60 Pro",
        "Sony WH-1000XM5", "Kindle Paperwhite", "Nintendo Switch",
        "Dyson吹风机", "Logitech MX Master 3", "Sony A7M4相机"
    ]
    
    for i in range(count):
        base_name = random.choice(product_names)
        product = {
            "id": i + 1,
            "name": f"{base_name} {fake.color_name()}限定版",
            "price": random.randint(99, 19999),
            "stock": random.randint(0, 1000),  # 包含0库存，测边界
            "category": random.choice(["数码", "家电", "图书", "游戏"]),
            "created_at": fake.date_time_this_year().isoformat()
        }
        products.append(product)
    return products

def generate_orders(users, products, count=500):
    """生成测试订单数据"""
    orders = []
    statuses = ['created', 'paid', 'shipped', 'completed', 'cancelled']
    
    for i in range(count):
        user = random.choice(users)
        product = random.choice(products)
        amount = random.randint(1, 10)
        
        order = {
            "id": 1000 + i,
            "user_id": user["id"],
            "username": user["username"],
            "product_id": product["id"],
            "product_name": product["name"],
            "amount": amount,
            "total_price": product["price"] * amount,
            "status": random.choice(statuses),
            "created_at": fake.date_time_this_month().isoformat()
        }
        orders.append(order)
    return orders

if __name__ == "__main__":
    # 生成数据
    users = generate_users(50)
    products = generate_products(20)
    orders = generate_orders(users, products, 200)
    
    # 保存为JSON（给接口测试用）
    with open("test_data/generated_users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    
    with open("test_data/generated_products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    with open("test_data/generated_orders.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成：{len(users)}个用户，{len(products)}个商品，{len(orders)}个订单")
    print("💡 查看 test_data/ 目录下的JSON文件")