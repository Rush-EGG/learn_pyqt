class Scheduler(object):
    def __init__(self):
        self.thread_list = []

    def start(self):
        # 1.获取表格中所有数据，为每一行都去创建一个线程进行监控
        # 2.每个线程 执行 也要将状态实时的显示在表格中 利用信号+回调
        pass

    def stop(self):
        pass


# 单例模式
SCHEDULER = Scheduler()
