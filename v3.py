import os
import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QMenu
from utils.threads import NewTaskThread
from utils.dialog import AlertDialog, ProxyDialog, LogDialog
from utils.scheduler import SCHEDULER

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

STATUS_MAPPING = {
    0: "初始化中",
    1: "待执行",
    2: "正在执行",
    11: "初始化失败",
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 控件
        self.txt_asin = None

        # 窗体标题
        self.setWindowTitle('NB的xx系统')

        # 窗体尺寸
        self.resize(1268, 450)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 创建垂直方向的布局
        layout = QVBoxLayout()

        # 1.创建顶部菜单布局
        layout.addLayout(self.init_header())
        # 2.创建表单布局
        layout.addLayout(self.init_form())
        # 3.创建表格布局
        layout.addLayout(self.init_table())
        # 4.创建底部菜单布局
        layout.addLayout(self.init_bottom())
        # 底部加入弹簧
        # layout.addStretch()

        # 给窗体设置元素的排列方式
        self.setLayout(layout)

    def init_header(self):
        header_layout = QHBoxLayout()

        # 创建两个按钮，加入到header_layout
        btn_start = QPushButton("开始")
        # btn_start.setFixedWidth(200)  # 设置宽度
        btn_start.clicked.connect(self.event_start_click)
        header_layout.addWidget(btn_start)
        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.event_stop_click)
        header_layout.addWidget(btn_stop)

        # 右侧加入弹簧
        header_layout.addStretch()

        return header_layout

    def init_form(self):
        form_layout = QHBoxLayout()
        # 输入框
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ID和价格，如：100016046824=80")  # 添加输入框提示文字
        self.txt_asin = txt_asin
        form_layout.addWidget(txt_asin)
        # 按钮
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)
        form_layout.addWidget(btn_add)

        return form_layout

    def init_table(self):
        table_layout = QHBoxLayout()
        # 0行8列的表格
        self.table_widget = table_widget = QTableWidget(0, 8)

        # 表格标题元组
        table_header = [
            {'filed': 'asin', 'text': 'ASIN', 'width': 120},
            {'filed': 'title', 'text': "标题", 'width': 160},
            {'filed': 'url', 'text': 'URL', 'width': 400},
            {'filed': 'price', 'text': "底价", 'width': 100},
            {'filed': 'success', 'text': "成功次数", 'width': 100},
            {'filed': 'error', 'text': "503次数", 'width': 100},
            {'filed': 'status', 'text': "状态", 'width': 100},
            {'filed': 'frequency', 'text': "频率（N秒/次）", 'width': 130},
        ]
        # 循环设置表格标题
        for idx, info in enumerate(table_header):
            # 创建表格标题对象
            item = QTableWidgetItem()
            item.setText(info['text'])
            table_widget.setHorizontalHeaderItem(idx, item)
            table_widget.setColumnWidth(idx, info['width'])

        # 在表格种添加数据
        # 读取数据文件
        file_path = os.path.join(BASE_DIR, 'db', 'db.json')
        with open(file_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        data_list = json.loads(data)
        # print(data_list)

        current_row_count = table_widget.rowCount()  # 获取当前表格有多少行
        for row_list in data_list:
            # 添加新的一行
            table_widget.insertRow(current_row_count)
            for i, ele in enumerate(row_list):
                if i == 6:  # 修改状态在表格中的体现形式
                    ele = STATUS_MAPPING[ele]
                # 创建一个单元格
                ceil = QTableWidgetItem(str(ele))
                # 设置单元格不可修改
                if i in [0, 4, 5, 6]:
                    ceil.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # 三个参数分别是：行，列，内容
                table_widget.setItem(current_row_count, i, ceil)

            current_row_count += 1

        # 开启右键菜单，其实也是绑定函数
        table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.table_right_menu)

        table_layout.addWidget(table_widget)

        return table_layout

    def init_bottom(self):
        bottom_layout = QHBoxLayout()

        self.label_status = label_status = QLabel("未检测", self)
        bottom_layout.addWidget(label_status)

        # 添加弹簧
        bottom_layout.addStretch()

        btn_reset = QPushButton("重新初始化")
        btn_reset.clicked.connect(self.event_reset_click)
        bottom_layout.addWidget(btn_reset)

        btn_recheck = QPushButton("重新检测")
        bottom_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton("次数清零")
        btn_reset_count.clicked.connect(self.event_reset_count_click)
        bottom_layout.addWidget(btn_reset_count)

        btn_delete = QPushButton("删除检测项")
        btn_delete.clicked.connect(self.event_delete_click)
        bottom_layout.addWidget(btn_delete)

        btn_alert = QPushButton("SMTP报警配置")
        btn_alert.clicked.connect(self.event_alert_click)
        bottom_layout.addWidget(btn_alert)

        btn_proxy = QPushButton("代理IP")
        btn_proxy.clicked.connect(self.event_proxy_click)
        bottom_layout.addWidget(btn_proxy)

        return bottom_layout

    # 点击添加按钮
    def event_add_click(self):
        # 获取输入框中的内容
        text = self.txt_asin.text()
        # 去除空格
        text = text.strip()
        # 如果为空，报错
        if not text:
            QMessageBox.warning(self, "错误", "商品的ASIN格式有误")
            return
        # text = 100016046824=80
        asin, price = text.split("=")  # asin=100016046824
        price = float(price)  # price=80.0

        # 加入到表格中（型号、底价）
        new_row_list = [asin, "", "", price, 0, 0, 0, 5]
        # 获取当前已有的行数
        current_row_count = self.table_widget.rowCount()
        # 插入新的一行
        self.table_widget.insertRow(current_row_count)
        for i, ele in enumerate(new_row_list):
            if i == 6:  # 修改状态在表格中的体现形式
                ele = STATUS_MAPPING[ele]
            # 创建一个单元格
            ceil = QTableWidgetItem(str(ele))
            # 设置单元格不可修改
            if i in [0, 4, 5, 6]:
                ceil.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            # 三个参数分别是：行，列，内容
            self.table_widget.setItem(current_row_count, i, ceil)

        # 通过爬虫发送请求获取标题
        # 注意不能在主线程中做这种事，而是应该创建一个线程，再更新到窗体应用中
        thread = NewTaskThread(current_row_count, asin, self)
        thread.success.connect(self.init_task_success_callback)
        thread.error.connect(self.init_task_error_callback)
        thread.start()

    def init_task_success_callback(self, row_index, asin, title, url):
        # 更新窗体显示数据
        print(row_index, asin, title, url)

        # 更新窗体的标题，第一列
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新url，第二列
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态列，第六列
        cell_status = QTableWidgetItem(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)

        # 清空输入框
        self.txt_asin.clear()

    def init_task_error_callback(self, row_index, asin, title, url):
        # 更新窗体的标题，第一列
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新url，第二列
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态列
        cell_status = QTableWidgetItem(STATUS_MAPPING[11])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)

    # 点击重新初始化
    def event_reset_click(self):
        # 获取已选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择一行或多行数据！")
            return
        # 对选中的行进行初始化
        for row_object in row_list:
            index = row_object.row()
            # print("选中的行", index)
            # 获取型号
            asin = self.table_widget.item(index, 0).text().strip()
            # 改变状态
            cell_status = QTableWidgetItem(STATUS_MAPPING[0])
            cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 6, cell_status)

            # 创建线程去做初始化
            thread = NewTaskThread(index, asin, self)
            thread.success.connect(self.init_task_success_callback)
            thread.error.connect(self.init_task_error_callback)
            thread.start()

    # 次数清零
    def event_reset_count_click(self):
        # 获取已选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择一行或多行数据！")
            return
        # 对选中的行进行初始化
        for row_object in row_list:
            index = row_object.row()
            # 对数量做清零
            cell_success = QTableWidgetItem(str(0))
            cell_success.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 4, cell_success)

            cell_error = QTableWidgetItem(str(0))
            cell_error.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 5, cell_error)

    # 删除操作
    def event_delete_click(self):
        # 获取已选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择一行或多行数据！")
            return
        # 做删除时最好是倒序删除，所以要反转一下
        row_list.reverse()
        for row_object in row_list:
            index = row_object.row()
            self.table_widget.removeRow(index)

    # 报警弹窗
    def event_alert_click(self):
        # 创建弹窗
        dialog = AlertDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    # 代理弹窗
    def event_proxy_click(self):
        # 创建弹窗
        dialog = ProxyDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    # 表格右击菜单
    def table_right_menu(self, pos):
        # 只有选中行了，才能右键
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) == 0:
            return
        # 如果选中多行，通过selected_item_list[0]来指定选中的第一行

        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_log = menu.addAction("查看日志")
        item_log_clear = menu.addAction("清除日志")
        # 选中了哪个
        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        if action == item_copy:
            # 复制选中行的型号
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item_list[0].text())

        if action == item_log:
            # 获取选中的型号
            row_index = selected_item_list[0].row()
            asin = self.table_widget.item(row_index, 0).text().strip()
            # 在对话框显示日志对话框
            dialog = LogDialog(asin)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()

        if action == item_log_clear:
            # 获取选中的型号
            row_index = selected_item_list[0].row()
            asin = self.table_widget.item(row_index, 0).text().strip()
            # 删除日志文件
            file_path = os.path.join("log", "{}.log".format(asin))
            if os.path.exists(file_path):
                os.remove(file_path)

    # 点击开始
    def event_start_click(self):
        # 1.为每一行创建线程 (记录所有的线程，便于后续的停止）
        SCHEDULER.start()
        # 2.修改状态为：执行中
        self.update_status_message("执行中")

    def event_stop_click(self):
        # 1.让执行中的线程逐一中止
        SCHEDULER.stop()
        # 2.修改状态为：***
        pass

    def update_status_message(self, message):
        self.label_status.setText(message)
        self.label_status.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
