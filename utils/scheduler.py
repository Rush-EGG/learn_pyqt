import os
from utils.threads import TaskThread, StopThread


class Scheduler(object):
    def __init__(self):
        self.thread_list = []
        self.window = None
        self.terminate = False  # 是否点击停止按钮

    def start(self, base_dir, window, fn_start, fn_stop, fn_counter, fn_error_counter):
        self.window = window
        self.terminate = False
        # 1.获取表格中所有数据，为每一行都去创建一个线程进行监控
        for row_index in range(window.table_widget.rowCount()):
            # 0/1/2
            asin = window.table_widget.item(row_index, 0).text().strip()
            status_text = window.table_widget.item(row_index, 6).text().strip()

            # 创建日志文件目录
            log_folder = os.path.join(base_dir, 'log')
            if not os.path.exists(log_folder):
                os.makedirs(log_folder)
            log_file_path = os.path.join(log_folder, "{}.log".format(asin))

            # 只有是待执行状态的才创建线程
            if status_text != "待执行":
                continue
            # 2.每个线程 执行 也要将状态实时的显示在表格中 利用信号+回调
            t = TaskThread(self, log_file_path, row_index, asin, window)
            # 把函数传递给线程，让线程帮忙完成对状态的更新
            t.start_signal.connect(fn_start)
            t.stop_signal.connect(fn_stop)
            # 把函数传递给线程，让线程帮忙完成对个数的更新
            t.counter_signal.connect(fn_counter)
            # 把函数传递给线程，让线程帮忙完成对错误个数的更新
            t.error_counter_signal.connect(fn_error_counter)
            t.start()

            # 添加新线程进线程列表
            self.thread_list.append(t)

    def stop(self):
        self.terminate = True
        # 创建线程，监测thread_list中的数量，并实时的更新到窗体的label中
        t = StopThread(self, self.window)
        t.update_signal.connect(self.window.update_status_message)
        t.start()

    def destroy_thread(self, thread):
        self.thread_list.remove(thread)


# 单例模式
SCHEDULER = Scheduler()
