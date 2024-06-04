import os
import re
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from utils import jsonUtils
from utils.excel_export import excel_export

# 定义路径
driver_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '\\msedgedriver.exe'
project_data_file = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\data\\project_data.json"

# 数据
data_list = []


def get_project_data():
    return jsonUtils.parse_file_to_map(project_data_file)


def open_edge():
    driver = None
    try:
        service = Service(executable_path=driver_path)
        with webdriver.Edge(service=service) as driver:
            print("浏览器开启成功")
            use_data(driver)
    except WebDriverException as e:
        print("打开浏览器错误:", e)
    finally:
        if driver:
            driver.quit()


def construct_data(title, href, date):
    global data_list
    data = {
        "title": title,
        "href": href,
        "date": date
    }
    data_list.append(data)


def one(data, driver):
    # https://zzcg.sz-mtr.com/cgxx/002002/sort.html
    try:
        driver.get(data["website"])
        main_page = WebDriverWait(driver, 10)  # 最多等待 10 秒
        input_element = driver.find_element(By.ID, 'Keyword')
        search_element = driver.find_element(By.CSS_SELECTOR, '.search-btn.l')
        for keyword in data["keywords"]:
            input_element.clear()
            input_element.send_keys(keyword)
            search_element.click()
            time.sleep(3)
            # 获取ul元素
            parent_element = driver.find_element(By.ID, 'infolist')
            li_elements = parent_element.find_elements(By.TAG_NAME, 'li')
            # 输出所有<li>元素的内容
            for li_element in li_elements:
                a_element = li_element.find_element(By.CSS_SELECTOR, 'a[class*=notice-name]')
                title = a_element.text
                href = a_element.get_attribute('href')
                text = li_element.get_attribute('outerHTML')
                match = re.search(r'发布日期：\d{4}-\d{2}-\d{2}', text)
                date = match.group(0).replace('发布日期：', '')
                print(f"title：{title} href：{href} date：{date}")
                construct_data(title, href, date)

        time.sleep(5)
    except Exception as e:
        print("爬取数据出错:", e)


def two(data, driver):
    # https://zhaotoubiao.sipac.gov.cn/szgyy/zfcg/002001/generalList.html
    try:
        driver.get(data["website"])
        main_page = WebDriverWait(driver, 10)  # 最多等待 10 秒
        input_element = driver.find_element(By.CSS_SELECTOR, 'input[class*=tit-name-input]')
        search_element = driver.find_element(By.CSS_SELECTOR, 'a[class*=right-tit-btn]')
        for keyword in data["keywords"]:
            input_element.clear()
            input_element.send_keys(keyword)
            search_element.click()
            time.sleep(3)
            # 获取ul元素
            parent_element = driver.find_element(By.ID, 'list')
            li_elements = parent_element.find_elements(By.TAG_NAME, 'li')
            # 输出所有<li>元素的内容
            for li_element in li_elements:
                a_element = li_element.find_element(By.TAG_NAME, 'a')
                title = a_element.text
                href = a_element.get_attribute('href')
                text = li_element.get_attribute('outerHTML')
                match = re.search(r'\d{4}-\d{2}-\d{2}', text)
                date = match.group(0)
                print(f"title：{title} href：{href} date：{date}")
                construct_data(title, href, date)

        time.sleep(5)
    except Exception as e:
        print("爬取数据出错:", e)


def three(data, driver):
    # https://czju.suzhou.gov.cn/zfcg/html/main/index.shtml
    try:
        driver.get(data["website"])
        main_page = WebDriverWait(driver, 10)  # 最多等待 10 秒
        input_element = driver.find_element(By.ID, 'titles')
        search_element = driver.find_element(By.CSS_SELECTOR, 'input[class*=button]')
        for keyword in data["keywords"]:
            input_element.clear()
            input_element.send_keys(keyword)
            search_element.click()
            time.sleep(5)
            # 找到父元素
            parent_element = driver.find_element(By.ID, 'searchid')
            # 提取所有的子元素<li>
            li_elements = parent_element.find_elements(By.TAG_NAME, 'li')
            # 输出所有<li>元素的内容
            for li_element in li_elements:
                # 提取标题、链接和日期信息
                title = li_element.find_element(By.TAG_NAME, 'a').get_attribute('title')
                href = li_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                date = li_element.find_element(By.CLASS_NAME, 'L_date').text.strip('[] ')
                print(f"title：{title} href：{href} date：{date}")
                construct_data(title, href, date)
            driver.back()

        time.sleep(5)
    except Exception as e:
        print("爬取数据出错:", e)


def use_data(driver):
    global data_list
    projects = get_project_data()["projects"]

    if len(projects) == 0:
        print("数据为空,请先添加数据!")
        return

    print("数据获取成功")
    print("开始爬取数据")

    for data in projects:
        if data["website"] == "https://zzcg.sz-mtr.com/cgxx/002002/sort.html":
            one(data, driver)
        elif data["website"] == "https://zhaotoubiao.sipac.gov.cn/szgyy/zfcg/002001/generalList.html":
            two(data, driver)

        elif data["website"] == "https://zhaotoubiao.sipac.gov.cn/szgyy/gyjtqycg/003001/generalList.html":
            two(data, driver)
        elif data["website"] == "https://czju.suzhou.gov.cn/zfcg/html/main/index.shtml":
            three(data, driver)
        else:
            print("当前网站未适配")
    print("爬取结束")
    print(data_list)
    excel_export(data_list)


if __name__ == '__main__':
    open_edge()
