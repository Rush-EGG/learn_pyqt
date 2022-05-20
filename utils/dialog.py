import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QHBoxLayout


class AlertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_dict = {}
        self.init_ui()

    def init_ui(self):
        # 初始化对话框
        self.setWindowTitle("报警邮件配置")
        self.resize(300, 270)

        layout = QVBoxLayout()

        form_data_list = [
            {'title': "SMTP服务器", 'field': 'smtp'},
            {'title': "发件箱", 'field': 'from'},
            {'title': "密码", 'field': 'pwd'},
            {'title': "收件人（多个用逗号分割", 'field': 'to'},
        ]
        old_alert_dict = {}

        # 读取json文件中已保存的配置
        alert_file_path = os.path.join("db", 'alert.json')
        if os.path.exists(alert_file_path):
            file_object = open(os.path.join("db", 'alert.json'), mode='r', encoding='utf-8')
            old_alert_dict = json.load(file_object)
            file_object.close()

        # 遍历创建窗体内容
        for item in form_data_list:
            lbl = QLabel()
            lbl.setText(item['title'])
            layout.addWidget(lbl)

            txt = QLineEdit()
            layout.addWidget(txt)

            # 如果已经有写好的SMTP配置json文件，就将他作为弹窗输入行的默认值
            field = item['field']
            if old_alert_dict and field in old_alert_dict:
                txt.setText(old_alert_dict[field])
            self.field_dict[item['field']] = txt

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.event_save_click)
        layout.addWidget(btn_save, 0, Qt.AlignRight)

        layout.addStretch(1)
        self.setLayout(layout)

    def event_save_click(self):
        data_dict = {}

        for key, field in self.field_dict.items():
            value = field.text().strip()
            if not value:
                QMessageBox.warning(self, "错误", "邮件报警项不可为空！")
                return
            data_dict[key] = value

        print(data_dict)

        # 将输入的SMTP配置写入到json文件中
        file_object = open(os.path.join("db", 'alert.json'), mode='w', encoding='utf-8')
        json.dump(data_dict, file_object)
        file_object.close()

        self.close()


class ProxyDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        # 初始化对话框
        self.setWindowTitle("配置代理IP")
        self.resize(500, 400)
        layout = QVBoxLayout()

        # 输入框
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("可用换行来设置多个代理IP，每个代理IP设置格式为：31.40.255.250:3128")

        # 读取已经存好的代理IP
        all_proxy = ""
        file_path = os.path.join("db", "proxy.txt")
        if os.path.exists(file_path):  # 如果存在
            with open(os.path.join("db", "proxy.txt"), mode='r', encoding='utf-8') as f:
                all_proxy = f.read()
        text_edit.setText(all_proxy)

        self.text_edit = text_edit
        layout.addWidget(text_edit)

        footer_config = QHBoxLayout()

        btn_save = QPushButton("重置")
        btn_save.clicked.connect(self.event_save_click)
        footer_config.addWidget(btn_save, 0, Qt.AlignRight)

        layout.addLayout(footer_config)

        self.setLayout(layout)

    def event_save_click(self):
        text = self.text_edit.toPlainText()
        # 写入到代理文件中
        with open(os.path.join("db", "proxy.txt"), mode='w', encoding='utf-8') as f:
            f.write(text)

        self.close()


class LogDialog(QDialog):
    def __init__(self, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin

        self.init_ui()

    def init_ui(self):
        # 初始化对话框
        self.setWindowTitle("日志记录")
        self.resize(500, 400)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setText("")
        layout.addWidget(text_edit)

        self.setLayout(layout)

        file_path = os.path.join("log", "{}.log".format(self.asin))
        if not os.path.exists(file_path):
            return

        with open(file_path, mode='r', encoding='utf-8') as f:
            content = f.read()
        text_edit.setText(content)
