import os
import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QTableWidget, QTableWidgetItem, QLabel

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

STATUS_MAPPING = {
    0: "初始化中",
    1: "待执行",
    2: "正在执行",
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

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
        header_layout.addWidget(btn_start)
        btn_stop = QPushButton("停止")
        header_layout.addWidget(btn_stop)

        # 右侧加入弹簧
        header_layout.addStretch()

        return header_layout

    def init_form(self):
        form_layout = QHBoxLayout()
        # 输入框
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ID和价格，如：B018JJQQ8=88")  # 添加输入框提示文字
        form_layout.addWidget(txt_asin)
        # 按钮
        btn_add = QPushButton("添加")
        form_layout.addWidget(btn_add)

        return form_layout

    def init_table(self):
        table_layout = QHBoxLayout()
        # 0行8列的表格
        table_widget = QTableWidget(0, 8)

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

        table_layout.addWidget(table_widget)

        return table_layout

    def init_bottom(self):
        bottom_layout = QHBoxLayout()

        label_status = QLabel("未检测", self)
        bottom_layout.addWidget(label_status)

        # 添加弹簧
        bottom_layout.addStretch()

        btn_reinit = QPushButton("重新初始化")
        bottom_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton("重新检测")
        bottom_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton("次数清零")
        bottom_layout.addWidget(btn_reset_count)

        btn_delete = QPushButton("删除检测项")
        bottom_layout.addWidget(btn_delete)

        btn_alert = QPushButton("SMTP报警配置")
        bottom_layout.addWidget(btn_alert)

        btn_proxy = QPushButton("代理IP")
        bottom_layout.addWidget(btn_proxy)

        return bottom_layout


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
