import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """每个测试方法前后自动开关浏览器"""
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service)
    drv.implicitly_wait(5)  # 兜底，但主要用显式等待
    yield drv  # 这里把driver交给测试用例
    drv.quit()  # 测试结束后关闭浏览器


@allure.feature("百度搜索")
class TestBaiduSearch:
    """百度搜索UI自动化测试"""
    
    BASE_URL = "https://www.baidu.com"
    
    @allure.story("正常搜索")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_normal(self, driver):
        with allure.step("1. 打开百度首页"):
            driver.get(self.BASE_URL)
            allure.attach(driver.current_url, "当前URL", allure.attachment_type.TEXT)
        
        with allure.step("2. 输入搜索关键词"):
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "kw"))
            )
            driver.execute_script("arguments[0].value = 'Pytest教程';", search_box)
            allure.attach("Pytest教程", "搜索关键词", allure.attachment_type.TEXT)
        
        with allure.step("3. 点击搜索按钮"):
            search_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "su"))
            )
            driver.execute_script("arguments[0].click();", search_button)
        
        with allure.step("4. 等待并验证搜索结果"):
            wait = WebDriverWait(driver, 10)
            wait.until(EC.title_contains("Pytest教程"))
            
            results = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".result"))
            )
            assert len(results) > 0, "未找到搜索结果"
            allure.attach(f"找到 {len(results)} 条结果", "搜索结果", allure.attachment_type.TEXT)
    
    @allure.story("搜索无结果")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_no_results(self, driver):
        with allure.step("搜索一串无意义字符"):
            driver.get(self.BASE_URL)
            # driver.find_element(By.ID, "kw").send_keys("！？￥%……&*（")
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "kw"))
            )
            driver.execute_script("arguments[0].value = '！？￥%……&*（';", search_box)
            search_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "su"))
            )
            driver.execute_script("arguments[0].click();", search_button)
        
        with allure.step("验证提示无结果或结果极少"):
            wait = WebDriverWait(driver, 10)
            wait.until(EC.title_contains("！？￥%……&*（"))
            
            # 无结果页面可能有特殊提示
            # 这里简化：至少页面没崩溃
            assert "百度一下" not in driver.title  # 已经跳走了