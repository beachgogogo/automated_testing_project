from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://www.baidu.com")
    
    # 用CSS Selector定位搜索框
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kw"))
    )

    # ========== 4. 用 JS 直接设值，绕过遮挡 ==========
    driver.execute_script("arguments[0].value = 'Selenium教程';", search_box)
    
    # ========== 5. 同样用 JS 点击搜索按钮 ==========
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "su"))
    )
    driver.execute_script("arguments[0].click();", search_button)

    # ========== 6. 等待搜索结果 ==========
    WebDriverWait(driver, 10).until(
        EC.title_contains("Selenium教程")
    )
        
    # 断言标题
    assert "Selenium教程" in driver.title
    print("页面标题包含 Selenium教程")
    
    # 额外验证：搜索结果页有没有结果列表
    results = driver.find_elements(By.CSS_SELECTOR, ".result")
    print(f"找到 {len(results)} 条搜索结果")
    assert len(results) > 0, "没有搜索结果"
    
finally:
    driver.quit()
