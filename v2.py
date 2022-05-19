import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QTableWidget, QTableWidgetItem, QLabel


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
            {'filed': 'title', 'text': "标题", 'width': 150},
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
