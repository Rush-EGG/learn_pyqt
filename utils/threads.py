import time
import random
import bs4
import requests
from bs4 import BeautifulSoup
import lxml
from PyQt5.QtCore import QThread, pyqtSignal

HOST = "https://www.amazon.com/"
HOST_ASIN_TPL = "{}{}".format(HOST, "gp/product/")
HOST_TASK_LIST_TPL = "{}{}".format(HOST, "gp/offer-listing")


class NewTaskThread(QThread):
    # 创建信号，触发信号来更新窗体中的数据
    success = pyqtSignal(int, str, str, str)
    error = pyqtSignal(int, str, str, str)

    def __init__(self, row_index, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_index = row_index
        self.asin = asin

    def run(self):
        # 线程应该做的事
        try:
            # 根据输入去拼接url
            url = "{}{}/".format(HOST_ASIN_TPL, self.asin)
            print(url)
            res = requests.get(
                url=url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
                    "pragma": "no-cache",
                    "upgrade-insecure-requests": "1",
                    "cache-control": "no-cache",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "accept-encoding": "gzip, deflate, br",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                }
            )
            if res.status_code != 200:
                raise Exception("初始化失败")

            soup = bs4.BeautifulSoup(res.text, 'lxml')
            title = soup.find(id="productTitle").text.strip()
            tpl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_NEW_mbc?asin={}&m=&qid=1653029021&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=8-1&pc=dp&experienceId=aodAjaxMain"
            url = tpl.format(self.asin)
            # 获取到title和url，将这个信息填写到表格中
            self.success.emit(self.row_index, self.asin, title, url)
        except Exception as e:
            title = "监控项 {} 添加失败".format(self.asin)
            self.error.emit(self.row_index, self.asin, title, str(e))


class TaskThread(QThread):
    # 创建信号
    start_signal = pyqtSignal(int)
    stop_signal = pyqtSignal(int)
    counter_signal = pyqtSignal(int)
    error_counter_signal = pyqtSignal(int)

    def __init__(self, scheduler, log_file_path, row_index, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scheduler = scheduler
        self.log_file_path = log_file_path
        self.row_index = row_index
        self.asin = asin

    def run(self):
        # 触发start_signal
        self.start_signal.emit(self.row_index)

        # 每过1-3s完成对次数的更新
        while True:
            # 如果terminate是True就代表用户点击了停止
            if self.scheduler.terminate:
                self.stop_signal.emit(self.row_index)
                # 把自己从线程列表中移除掉
                self.scheduler.destroy_thread(self)
                return
            try:
                time.sleep(random.randint(1, 3))
                self.counter_signal.emit(self.row_index)

                with open(self.log_file_path, mode='a', encoding='utf-8') as f:
                    f.write("我是猪\n")

                # 监控
                # 1.根据型号访问链接并通过bs4获取数据
                # 2.监测价格是否低于预期
                # 3.发送报警
                time.sleep(5)
            except Exception as e:
                self.error_counter_signal.emit(self.row_index)


class StopThread(QThread):
    # 创建信号
    update_signal = pyqtSignal(str)

    def __init__(self, scheduler, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scheduler = scheduler

    def run(self):
        # 监测线程的数量
        total_count = len(self.scheduler.thread_list)
        while True:
            running_count = len(self.scheduler.thread_list)
            # 更新到页面上
            self.update_signal.emit("正在中止({})".format(running_count))

            if running_count == 0:
                break
            time.sleep(1)

        self.update_signal.emit("已全部终止")
