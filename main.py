import os
import threading

import webview

from utils import jsonUtils
from utils.webInfo import open_edge
from utils.win import set_auto_start

# 数据路径定义
setting_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data\\setting.json"
project_data_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data\\project_data.json"

# 定时器
interval_timer = None


def set_interval(func, interval):
    global interval_timer

    def wrapper():
        set_interval(func, interval)
        func()

    interval_timer = threading.Timer(interval, wrapper)
    interval_timer.start()
    return interval_timer


def set_timeout(func, delay):
    timer = threading.Timer(delay, func)
    timer.start()
    return timer


# 执行
def start_web():
    print("定时开始执行")
    open_edge()


class Api:

    def set_setting(self, data):
        print(f"设置：{data}")
        jsonUtils.json_write_to_file(data, setting_file)

        # 处理设置数据 TODO

        set_auto_start(data["isStart"])

        print(f"设置成功")

    def get_setting(self):
        print(f"获取设置")
        data = jsonUtils.parse_file_to_map(setting_file)
        print(f"获取成功：{data}")
        return data

    def set_project_data(self, data):
        print(f"加入项目：{data}")
        jsonUtils.json_write_to_file(data, project_data_file)
        print(f"项目加入成功")

    def get_project_data(self):
        print(f"获取项目列表")
        data = jsonUtils.parse_file_to_map(project_data_file)
        print(f"获取成功：{data}")
        return data

    def start(self):
        global interval_timer
        print("开始执行爬虫程序")
        frequency = int(jsonUtils.parse_file_to_map(setting_file)["frequency"])
        interval_timer = set_interval(start_web, frequency * 60 * 60)  # 10小时 = 10 * 60分钟 * 60秒
        # 先执行一次
        open_edge()

    def stop(self):
        global interval_timer
        if interval_timer is not None:
            interval_timer.cancel()
            print("停止执行爬虫程序")


if __name__ == '__main__':
    # 初始化API和webview窗口
    api = Api()

    # 构建HTML文件的路径
    html_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views/index.html')
    url = 'file://' + html_file_path

    g_window = webview.create_window('网站爬取工具', url=url, js_api=api, width=1430, height=900)
    # webview.start(debug=True)
    webview.start()
