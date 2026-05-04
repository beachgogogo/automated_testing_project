from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ========== 1. 启动浏览器 ==========
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'  # 只等 DOM 就绪，不等图片等资源
driver = webdriver.Chrome(service=service, options=options)

# ========== 2. 打开百度 ==========
driver.get("https://www.baidu.com")
print(f"当前页面标题: {driver.title}")

# ========== 3. 等待搜索框在 DOM 中出现 ==========
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "kw"))
)

# ========== 4. 用 JS 直接设值，绕过遮挡 ==========
driver.execute_script("arguments[0].value = '软件测试';", search_box)

# ========== 5. 同样用 JS 点击搜索按钮 ==========
search_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "su"))
)
driver.execute_script("arguments[0].click();", search_button)

# ========== 6. 等待搜索结果 ==========
WebDriverWait(driver, 10).until(
    EC.title_contains("软件测试")
)

# ========== 7. 断言 ==========
assert "软件测试" in driver.title, f"标题中没有'软件测试'，实际标题: {driver.title}"
print("断言通过！页面标题包含'软件测试'")

# ========== 8. 关闭浏览器 ==========
driver.quit()