import sys
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox,
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QComboBox, QWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor
from network_manager import NetworkManager, NetworkConfig
import os

class NetworkConfigDialog(QDialog):
    """网络配置对话框"""
    
    def __init__(self, parent=None, config=None, edit_mode=False):
        super().__init__(parent)
        self.config = config
        self.edit_mode = edit_mode
        self.init_ui()
        
        if config and edit_mode:
            self.load_config_data()
    
    def init_ui(self):
        self.setWindowTitle("编辑网络配置" if self.edit_mode else "新建网络配置")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        
        # 配置名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("配置名称:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # DHCP选项
        self.dhcp_checkbox = QCheckBox("使用DHCP自动获取")
        self.dhcp_checkbox.stateChanged.connect(self.on_dhcp_changed)
        layout.addWidget(self.dhcp_checkbox)
        
        # 静态IP配置组
        self.static_widget = QWidget()
        static_layout = QVBoxLayout()
        
        # IP地址
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("IP地址:"))
        self.ip_edit = QLineEdit()
        ip_layout.addWidget(self.ip_edit)
        static_layout.addLayout(ip_layout)
        
        # 子网掩码
        subnet_layout = QHBoxLayout()
        subnet_layout.addWidget(QLabel("子网掩码:"))
        self.subnet_edit = QLineEdit()
        self.subnet_edit.setText("255.255.255.0")
        subnet_layout.addWidget(self.subnet_edit)
        static_layout.addLayout(subnet_layout)
        
        # 默认网关
        gateway_layout = QHBoxLayout()
        gateway_layout.addWidget(QLabel("默认网关:"))
        self.gateway_edit = QLineEdit()
        gateway_layout.addWidget(self.gateway_edit)
        static_layout.addLayout(gateway_layout)
        
        # DNS服务器
        dns1_layout = QHBoxLayout()
        dns1_layout.addWidget(QLabel("首选DNS:"))
        self.dns1_edit = QLineEdit()
        dns1_layout.addWidget(self.dns1_edit)
        static_layout.addLayout(dns1_layout)
        
        dns2_layout = QHBoxLayout()
        dns2_layout.addWidget(QLabel("备用DNS:"))
        self.dns2_edit = QLineEdit()
        dns2_layout.addWidget(self.dns2_edit)
        static_layout.addLayout(dns2_layout)
        
        self.static_widget.setLayout(static_layout)
        layout.addWidget(self.static_widget)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def on_dhcp_changed(self, state):
        """DHCP选项改变时的处理"""
        self.static_widget.setEnabled(state != Qt.Checked)
    
    def load_config_data(self):
        """加载配置数据到界面"""
        if self.config:
            self.name_edit.setText(self.config.name)
            self.dhcp_checkbox.setChecked(self.config.dhcp)
            
            if not self.config.dhcp:
                if self.config.ip:
                    self.ip_edit.setText(self.config.ip)
                if self.config.subnet:
                    self.subnet_edit.setText(self.config.subnet)
                if self.config.gateway:
                    self.gateway_edit.setText(self.config.gateway)
                if self.config.dns1:
                    self.dns1_edit.setText(self.config.dns1)
                if self.config.dns2:
                    self.dns2_edit.setText(self.config.dns2)
    
    def get_config(self):
        """获取配置数据"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "请输入配置名称")
            return None
        
        dhcp = self.dhcp_checkbox.isChecked()
        
        if dhcp:
            return NetworkConfig(name=name, dhcp=True)
        else:
            ip = self.ip_edit.text().strip()
            subnet = self.subnet_edit.text().strip()
            gateway = self.gateway_edit.text().strip()
            dns1 = self.dns1_edit.text().strip()
            dns2 = self.dns2_edit.text().strip()
            
            if not ip:
                QMessageBox.warning(self, "警告", "请输入IP地址")
                return None
            
            return NetworkConfig(
                name=name,
                ip=ip if ip else None,
                subnet=subnet if subnet else None,
                gateway=gateway if gateway else None,
                dns1=dns1 if dns1 else None,
                dns2=dns2 if dns2 else None,
                dhcp=False
            )

class AdapterSelectionDialog(QDialog):
    """网络适配器选择对话框"""
    
    def __init__(self, adapters, parent=None):
        super().__init__(parent)
        self.adapters = adapters
        self.selected_adapter = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("选择网络适配器")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("请选择要配置的网络适配器:"))
        
        self.adapter_combo = QComboBox()
        for adapter in self.adapters:
            self.adapter_combo.addItem(str(adapter), adapter)
        
        layout.addWidget(self.adapter_combo)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_selected_adapter(self):
        """获取选中的适配器"""
        return self.adapter_combo.currentData()

class SystemTrayApp:
    """系统托盘应用"""
    
    def __init__(self, network_manager):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        self.network_manager = network_manager
        self.current_adapter = None
        self.main_window = None
        
        # 检查系统托盘支持
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "系统托盘", "系统不支持托盘功能")
            sys.exit(1)
        
        # 自动选择第一个可用适配器
        self.auto_select_adapter()
        
        self.init_tray()
        
        # 初始化主界面
        self.init_main_window()
    
    def auto_select_adapter(self):
        """自动选择第一个可用的适配器"""
        adapters = self.network_manager.get_network_adapters()
        if adapters:
            self.current_adapter = adapters[0]
            print(f"自动选择适配器: {self.current_adapter.name}")
        else:
            print("未找到可用的网络适配器")
    
    def create_icon(self):
        """创建托盘图标"""
        # 创建一个简单的网络图标
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制网络图标
        painter.setBrush(QBrush(QColor(0, 120, 215)))
        painter.setPen(QColor(0, 120, 215))
        
        # 绘制简单的网络图标
        painter.drawEllipse(2, 2, 4, 4)
        painter.drawEllipse(10, 2, 4, 4)
        painter.drawEllipse(2, 10, 4, 4)
        painter.drawEllipse(10, 10, 4, 4)
        
        painter.drawLine(6, 4, 10, 4)
        painter.drawLine(6, 12, 10, 12)
        painter.drawLine(4, 6, 4, 10)
        painter.drawLine(12, 6, 12, 10)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.create_icon())
        self.tray_icon.setToolTip("网络配置切换工具")
        
        # 创建右键菜单
        self.create_menu()
        
        # 显示托盘图标
        self.tray_icon.show()
        
        # 连接信号
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def create_menu(self):
        """创建右键菜单"""
        menu = QMenu()
        
        # 主界面选项
        main_window_action = QAction("打开主界面", menu)
        main_window_action.triggered.connect(self.show_main_window)
        menu.addAction(main_window_action)
        
        menu.addSeparator()
        
        # 当前适配器信息
        if self.current_adapter:
            adapter_action = QAction(f"当前适配器: {self.current_adapter.description}", menu)
            adapter_action.setEnabled(False)
            menu.addAction(adapter_action)
            menu.addSeparator()
        
        # 网络配置选项
        for config in self.network_manager.configs:
            action = QAction(config.name, menu)
            action.triggered.connect(lambda checked, c=config: self.apply_config(c))
            menu.addAction(action)
        
        menu.addSeparator()
        
        # 管理选项
        new_config_action = QAction("新建配置", menu)
        new_config_action.triggered.connect(self.new_config)
        menu.addAction(new_config_action)
        
        edit_config_action = QAction("编辑配置", menu)
        edit_config_action.triggered.connect(self.edit_config)
        menu.addAction(edit_config_action)
        
        select_adapter_action = QAction("选择适配器", menu)
        select_adapter_action.triggered.connect(self.select_adapter)
        menu.addAction(select_adapter_action)
        
        menu.addSeparator()
        
        # 退出
        quit_action = QAction("退出", menu)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
    
    def select_adapter(self):
        """选择网络适配器"""
        adapters = self.network_manager.get_network_adapters()
        
        if not adapters:
            QMessageBox.warning(None, "警告", "未找到可用的网络适配器")
            return
        
        dialog = AdapterSelectionDialog(adapters)
        if dialog.exec_() == QDialog.Accepted:
            self.current_adapter = dialog.get_selected_adapter()
            self.create_menu()  # 重新创建菜单
            
            # 更新主界面
            if self.main_window:
                self.main_window.set_current_adapter(self.current_adapter)
    
    def apply_config(self, config):
        """应用网络配置"""
        if not self.current_adapter:
            QMessageBox.warning(None, "警告", "请先选择网络适配器")
            return
        
        try:
            success = self.network_manager.apply_config(self.current_adapter.name, config)
            if success:
                self.tray_icon.showMessage(
                    "网络配置",
                    f"已切换到配置: {config.name}",
                    QSystemTrayIcon.Information,
                    3000
                )
            else:
                self.tray_icon.showMessage(
                    "网络配置",
                    f"切换配置失败: {config.name}",
                    QSystemTrayIcon.Critical,
                    3000
                )
        except Exception as e:
            QMessageBox.critical(None, "错误", f"应用配置时发生错误: {str(e)}")
    
    def new_config(self):
        """新建配置"""
        dialog = NetworkConfigDialog()
        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            if config:
                self.network_manager.add_config(config)
                self.create_menu()  # 重新创建菜单
                QMessageBox.information(None, "成功", f"配置 '{config.name}' 已保存")
    
    def edit_config(self):
        """编辑配置"""
        if not self.network_manager.configs:
            QMessageBox.information(None, "提示", "没有可编辑的配置")
            return
        
        # 这里简化处理，编辑第一个非DHCP配置
        config_to_edit = None
        for config in self.network_manager.configs:
            if not config.dhcp:
                config_to_edit = config
                break
        
        if not config_to_edit:
            config_to_edit = self.network_manager.configs[0]
        
        dialog = NetworkConfigDialog(config=config_to_edit, edit_mode=True)
        if dialog.exec_() == QDialog.Accepted:
            new_config = dialog.get_config()
            if new_config:
                # 删除旧配置，添加新配置
                self.network_manager.remove_config(config_to_edit.name)
                self.network_manager.add_config(new_config)
                self.create_menu()  # 重新创建菜单
                QMessageBox.information(None, "成功", f"配置已更新")
    
    def init_main_window(self):
        """初始化主界面"""
        from main_window import MainWindow
        self.main_window = MainWindow(self.network_manager, self.current_adapter)
        self.main_window.tray_app = self  # 设置托盘应用引用
        # 程序启动时自动显示主界面
        self.main_window.show()
    
    def show_main_window(self):
        """显示主界面"""
        if self.main_window is None:
            self.init_main_window()
        
        self.main_window.set_current_adapter(self.current_adapter)
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
    
    def on_tray_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_main_window()
    
    def quit_app(self):
        """退出应用"""
        if self.main_window:
            self.main_window.close()
        self.tray_icon.hide()
        self.app.quit()
    
    def run(self):
        """运行应用"""
        return self.app.exec_()