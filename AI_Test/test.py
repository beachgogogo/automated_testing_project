import requests
import time
import pytest

# ==================== 配置区：只改这里 ====================
BASE_URL = "https://api.siliconflow.cn/v1"   # SiliconFlow的API地址
API_KEY = "sk-jlnlaffbxflraycfjcfpqipvccarmdrpqpsjghoxzgkdfaqh"                    # ← 填你从控制台复制的Key
MODEL = "deepseek-ai/DeepSeek-V4-Flash"             # 免费模型，效果好
# ========================================================

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_model_api_basic():
    """测试1：基础连通性 + 状态码 + 响应格式"""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "你好，请回复'测试通过'"}],
        "temperature": 0.1
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    
    # 断言1：状态码必须是200
    assert response.status_code == 200, f"状态码错误: {response.status_code}"
    
    # 断言2：必须是合法JSON
    data = response.json()
    
    # 断言3：关键字段必须存在（Schema校验）
    assert "choices" in data, "缺少 choices 字段"
    assert len(data["choices"]) > 0, "choices 为空"
    assert "message" in data["choices"][0], "缺少 message 字段"
    assert "content" in data["choices"][0]["message"], "缺少 content 字段"
    assert len(data["choices"][0]["message"]["content"]) > 0, "content 为空"
    
    # 断言4：模型路由正确（返回的model字段应该匹配请求）
    assert data.get("model") == MODEL, f"模型路由错误，请求{MODEL}，返回{data.get('model')}"
    
    print(f"\n✅ 响应内容: {data['choices'][0]['message']['content'][:50]}...")

def test_model_api_response_time():
    """测试2：响应时间性能测试"""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "Hello"}]
    }
    
    start = time.time()
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    elapsed = time.time() - start
    
    assert response.status_code == 200
    assert elapsed < 5.0, f"响应太慢了: {elapsed:.2f}s"  # 要求5秒内响应
    
    print(f"\n⏱️ 响应时间: {elapsed:.2f}s")

def test_model_api_usage_billing():
    """测试3：Usage字段完整性（计费相关）"""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "讲一个短笑话"}]
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    
    data = response.json()
    
    # 断言：计费相关字段必须存在
    assert "usage" in data, "缺少 usage 字段（无法计费）"
    assert "prompt_tokens" in data["usage"], "缺少 prompt_tokens"
    assert "completion_tokens" in data["usage"], "缺少 completion_tokens"
    assert data["usage"]["prompt_tokens"] > 0, "prompt_tokens 应该大于0"
    
    total = data["usage"]["prompt_tokens"] + data["usage"]["completion_tokens"]
    print(f"\n💰 Token消耗: prompt={data['usage']['prompt_tokens']}, completion={data['usage']['completion_tokens']}, total={total}")

def test_model_api_error_handling():
    """测试4：异常场景 - 错误的API Key"""
    bad_headers = {
        "Authorization": "Bearer sk-wrong-key-123456",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "test"}]
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=bad_headers,
        json=payload,
        timeout=10
    )
    
    # 断言：错误的Key应该返回401或403，不能是200
    assert response.status_code in [401, 403, 429], \
        f"错误鉴权应该被拒绝，实际状态码: {response.status_code}"
    
    print(f"\n🔒 错误Key已正确拦截，状态码: {response.status_code}")

def test_model_api_long_input():
    """测试5：边界测试 - 超长输入"""
    long_text = "请总结以下文本：" + "这是一个测试句子。" * 500  # 约3000字
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": long_text}]
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=HEADERS,
        json=payload,
        timeout=60
    )
    
    # 断言：超长输入不应该崩溃，要么成功，要么返回413/400
    assert response.status_code in [200, 400, 413], f"超长输入处理异常: {response.status_code}"
    
    if response.status_code == 200:
        data = response.json()
        assert "choices" in data
        print("\n📄 长文本处理成功")
    else:
        print(f"\n📄 长文本被合理拒绝，状态码: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])