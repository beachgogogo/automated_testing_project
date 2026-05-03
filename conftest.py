import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="session")
def base_url():
    """基础URL"""
    return BASE_URL

@pytest.fixture(scope="session")
def auth_token(base_url):
    """登录一次，整个测试session复用token"""
    payload = {"username": "admin", "password": "123456"}
    r = requests.post(f"{base_url}/api/login", json=payload)
    assert r.status_code == 200
    return r.json()["token"]

@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """带认证头的请求头"""
    return {"Authorization": f"Bearer {auth_token}"}