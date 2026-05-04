# shop_api_client.py - HTTP请求的"PageObject"
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        r = requests.post(f"{self.base_url}/api/login", json={
            "username": username, "password": password
        })
        if r.status_code == 200:
            self.token = r.json()["token"]
        return r
    
    def get_user_list(self):
        return requests.get(f"{self.base_url}/api/users")
    
    def get_user(self, num):
        return requests.get(f"{self.base_url}/api/users/{num}")
    
    def get_orders(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(f"{self.base_url}/api/orders", headers=headers)
    
    def get_orders_no_auth(self):
        return requests.get(f"{self.base_url}/api/orders")
    
    def create_order(self, product_id, amount):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.post(
            f"{self.base_url}/api/orders",
            headers=headers,
            json={"product_id": product_id, "amount": amount}
        )
    
    def get_product(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(f"{self.base_url}/api/products", headers=headers)

    def get_product_no_auth(self):
        return requests.get(f"{self.base_url}/api/products")
    