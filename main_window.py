#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主界面窗口
"""

import sys
import json
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QListWidget, QListWidgetItem,
    QMessageBox, QSplitter, QTextEdit, QFrame, QComboBox,
    QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from network_manager import NetworkManager, NetworkConfig
from system_tray import NetworkConfigDialog

class MainWindow(QMainWindow):
    """主界面窗口"""
    
    def __init__(self, network_manager, current_adapter=None):
        super().__init__()
        self.network_manager = network_manager
        self.current_adapter = current_adapter
        self.settings_file = 'app_settings.json'
        self.settings = self.load_settings()
        self.init_ui()
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_status)
        self.refresh_timer.start(5000)  # 每5秒刷新一次
        self.load_adapters()
        self.refresh_status()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("网络配置管理工具")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("网络配置管理工具")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧面板 - 当前状态
        self.create_status_panel(splitter)
        
        # 右侧面板 - 配置管理
        self.create_config_panel(splitter)
        
        # 底部按钮栏
        self.create_button_bar(main_layout)
        
        # 设置分割器比例
        splitter.setSizes([400, 400])
    
    def create_status_panel(self, parent):
        """创建状态面板"""
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        
        # 当前适配器信息
        adapter_group = QGroupBox("当前网络适配器")
        adapter_layout = QVBoxLayout(adapter_group)
        
        # 适配器选择下拉框
        adapter_select_layout = QHBoxLayout()
        adapter_select_layout.addWidget(QLabel("选择适配器:"))
        self.adapter_combo = QComboBox()
        self.adapter_combo.currentTextChanged.connect(self.on_adapter_changed)
        adapter_select_layout.addWidget(self.adapter_combo)
        adapter_layout.addLayout(adapter_select_layout)
        
        # 当前适配器详细信息
        self.adapter_detail_label = QLabel("未选择适配器")
        self.adapter_detail_label.setWordWrap(True)
        adapter_layout.addWidget(self.adapter_detail_label)
        
        status_layout.addWidget(adapter_group)
        
        # 当前网络配置
        config_group = QGroupBox("当前网络配置")
        config_layout = QVBoxLayout(config_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        config_layout.addWidget(self.status_text)
        
        refresh_btn = QPushButton("刷新状态")
        refresh_btn.clicked.connect(self.refresh_status)
        config_layout.addWidget(refresh_btn)
        
        status_layout.addWidget(config_group)
        
        # 网络连接测试
        test_group = QGroupBox("网络测试")
        test_layout = QVBoxLayout(test_group)
        
        test_btn = QPushButton("测试网络连接")
        test_btn.clicked.connect(self.test_network)
        test_layout.addWidget(test_btn)
        
        self.test_result = QLabel("点击按钮测试网络连接")
        self.test_result.setWordWrap(True)
        test_layout.addWidget(self.test_result)
        
        status_layout.addWidget(test_group)
        
        parent.addWidget(status_widget)
    
    def create_config_panel(self, parent):
        """创建配置面板"""
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        
        # 配置列表
        list_group = QGroupBox("网络配置模板")
        list_layout = QVBoxLayout(list_group)
        
        self.config_list = QListWidget()
        self.config_list.itemDoubleClicked.connect(self.apply_selected_config)
        list_layout.addWidget(self.config_list)
        
        # 配置操作按钮
        config_btn_layout = QHBoxLayout()
        
        apply_btn = QPushButton("应用配置")
        apply_btn.clicked.connect(self.apply_selected_config)
        config_btn_layout.addWidget(apply_btn)
        
        new_btn = QPushButton("新建配置")
        new_btn.clicked.connect(self.new_config)
        config_btn_layout.addWidget(new_btn)
        
        edit_btn = QPushButton("编辑配置")
        edit_btn.clicked.connect(self.edit_config)
        config_btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("删除配置")
        delete_btn.clicked.connect(self.delete_config)
        config_btn_layout.addWidget(delete_btn)
        
        list_layout.addLayout(config_btn_layout)
        config_layout.addWidget(list_group)
        
        # 配置详情
        detail_group = QGroupBox("配置详情")
        detail_layout = QVBoxLayout(detail_group)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumHeight(150)
        detail_layout.addWidget(self.detail_text)
        
        config_layout.addWidget(detail_group)
        
        parent.addWidget(config_widget)
    
    def create_button_bar(self, parent_layout):
        """创建底部按钮栏"""
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        parent_layout.addWidget(line)
        
        button_layout = QHBoxLayout()
        
        # 左侧信息
        info_label = QLabel("提示: 双击配置项可快速应用配置")
        info_label.setStyleSheet("color: gray;")
        button_layout.addWidget(info_label)
        
        button_layout.addStretch()
        
        # 右侧按钮
        minimize_btn = QPushButton("最小化到托盘")
        minimize_btn.clicked.connect(self.hide)
        button_layout.addWidget(minimize_btn)
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        parent_layout.addLayout(button_layout)
    
    def load_adapters(self):
        """加载网络适配器到下拉框"""
        adapters = self.network_manager.get_network_adapters()
        self.adapter_combo.clear()
        
        if adapters:
            # 添加适配器到下拉框
            for adapter in adapters:
                self.adapter_combo.addItem(f"{adapter.description}", adapter)
            
            # 设置当前适配器或默认选择第一个
            if self.current_adapter:
                for i in range(self.adapter_combo.count()):
                    adapter = self.adapter_combo.itemData(i)
                    if adapter and adapter.name == self.current_adapter.name:
                        self.adapter_combo.setCurrentIndex(i)
                        break
            else:
                # 默认选择第一个适配器
                if self.adapter_combo.count() > 0:
                    self.current_adapter = self.adapter_combo.itemData(0)
        else:
            self.adapter_combo.addItem("未找到可用适配器", None)
    
    def on_adapter_changed(self):
        """适配器选择改变"""
        current_adapter = self.adapter_combo.currentData()
        if current_adapter:
            self.current_adapter = current_adapter
            self.refresh_status()
    
    def refresh_status(self):
        """刷新状态信息"""
        # 更新适配器信息
        if self.current_adapter:
            self.adapter_detail_label.setText(
                f"名称: {self.current_adapter.name}\n"
                f"描述: {self.current_adapter.description}\n"
                f"索引: {self.current_adapter.index}"
            )
            
            # 获取当前配置
            current_config = self.network_manager.get_current_config(self.current_adapter.name)
            if current_config:
                status_text = "当前网络配置:\n\n"
                
                if current_config.get('dhcp', False):
                    status_text += "配置类型: DHCP (自动获取)\n"
                else:
                    status_text += "配置类型: 静态IP\n"
                    if 'ip' in current_config:
                        status_text += f"IP地址: {current_config['ip']}\n"
                    if 'subnet' in current_config:
                        status_text += f"子网掩码: {current_config['subnet']}\n"
                    if 'gateway' in current_config:
                        status_text += f"默认网关: {current_config['gateway']}\n"
                
                if 'dns1' in current_config:
                    status_text += f"首选DNS: {current_config['dns1']}\n"
                if 'dns2' in current_config:
                    status_text += f"备用DNS: {current_config['dns2']}\n"
                
                self.status_text.setText(status_text)
            else:
                self.status_text.setText("无法获取当前网络配置")
        else:
            self.adapter_detail_label.setText("未选择适配器")
            self.status_text.setText("请先选择网络适配器")
        
        # 更新配置列表
        self.refresh_config_list()
    
    def refresh_config_list(self):
        """刷新配置列表"""
        self.config_list.clear()
        
        for config in self.network_manager.configs:
            item = QListWidgetItem(config.name)
            item.setData(Qt.UserRole, config)
            self.config_list.addItem(item)
        
        # 选中第一项
        if self.config_list.count() > 0:
            self.config_list.setCurrentRow(0)
            self.show_config_detail()
        
        # 连接选择变化事件
        self.config_list.currentItemChanged.connect(self.on_config_selection_changed)
    
    def on_config_selection_changed(self):
        """配置选择变化"""
        self.show_config_detail()
    
    def show_config_detail(self):
        """显示配置详情"""
        current_item = self.config_list.currentItem()
        if current_item:
            config = current_item.data(Qt.UserRole)
            detail_text = f"配置名称: {config.name}\n\n"
            
            if config.dhcp:
                detail_text += "配置类型: DHCP (自动获取IP地址)\n"
            else:
                detail_text += "配置类型: 静态IP\n"
                if config.ip:
                    detail_text += f"IP地址: {config.ip}\n"
                if config.subnet:
                    detail_text += f"子网掩码: {config.subnet}\n"
                if config.gateway:
                    detail_text += f"默认网关: {config.gateway}\n"
                if config.dns1:
                    detail_text += f"首选DNS: {config.dns1}\n"
                if config.dns2:
                    detail_text += f"备用DNS: {config.dns2}\n"
            
            self.detail_text.setText(detail_text)
        else:
            self.detail_text.clear()
    
    def apply_selected_config(self):
        """应用选中的配置"""
        current_item = self.config_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择一个配置")
            return
        
        if not self.current_adapter:
            QMessageBox.warning(self, "警告", "请先选择网络适配器")
            return
        
        config = current_item.data(Qt.UserRole)
        
        try:
            success = self.network_manager.apply_config(self.current_adapter.name, config)
            if success:
                QMessageBox.information(self, "成功", f"已成功应用配置: {config.name}")
                # 延迟刷新状态
                QTimer.singleShot(2000, self.refresh_status)
            else:
                QMessageBox.critical(self, "失败", f"应用配置失败: {config.name}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"应用配置时发生错误: {str(e)}")
    
    def new_config(self):
        """新建配置"""
        dialog = NetworkConfigDialog(self)
        if dialog.exec_() == dialog.Accepted:
            config = dialog.get_config()
            if config:
                self.network_manager.add_config(config)
                self.refresh_config_list()
                QMessageBox.information(self, "成功", f"配置 '{config.name}' 已保存")
    
    def edit_config(self):
        """编辑配置"""
        current_item = self.config_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要编辑的配置")
            return
        
        config = current_item.data(Qt.UserRole)
        dialog = NetworkConfigDialog(self, config=config, edit_mode=True)
        if dialog.exec_() == dialog.Accepted:
            new_config = dialog.get_config()
            if new_config:
                # 删除旧配置，添加新配置
                self.network_manager.remove_config(config.name)
                self.network_manager.add_config(new_config)
                self.refresh_config_list()
                QMessageBox.information(self, "成功", "配置已更新")
    
    def delete_config(self):
        """删除配置"""
        current_item = self.config_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择要删除的配置")
            return
        
        config = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除配置 '{config.name}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.network_manager.remove_config(config.name)
            self.refresh_config_list()
            QMessageBox.information(self, "成功", f"配置 '{config.name}' 已删除")
    
    def load_settings(self):
        """加载应用设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载设置失败: {e}")
        
        # 默认设置
        return {
            'close_to_tray': True,  # 默认关闭到托盘
            'remember_choice': False
        }
    
    def save_settings(self):
        """保存应用设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")
    
    def test_network(self):
        """测试网络连接"""
        import subprocess
        import threading
        
        def run_test():
            try:
                self.test_result.setText("正在测试网络连接...")
                
                # 测试本地网关
                if self.current_adapter:
                    current_config = self.network_manager.get_current_config(self.current_adapter.name)
                    if current_config and 'gateway' in current_config:
                        gateway = current_config['gateway']
                        result = subprocess.run(
                            f'ping -n 1 -w 1000 {gateway}', 
                            shell=True, capture_output=True, text=True
                        )
                        if result.returncode == 0:
                            self.test_result.setText(f"✓ 网关连接正常 ({gateway})")
                        else:
                            self.test_result.setText(f"✗ 网关连接失败 ({gateway})")
                            return
                
                # 测试外网连接
                result = subprocess.run(
                    'ping -n 1 -w 3000 8.8.8.8', 
                    shell=True, capture_output=True, text=True
                )
                if result.returncode == 0:
                    self.test_result.setText("✓ 网络连接正常")
                else:
                    self.test_result.setText("✗ 无法连接到外网")
                    
            except Exception as e:
                self.test_result.setText(f"测试失败: {str(e)}")
        
        # 在后台线程运行测试
        threading.Thread(target=run_test, daemon=True).start()
    
    def set_current_adapter(self, adapter):
        """设置当前适配器"""
        self.current_adapter = adapter
        self.load_adapters()
        self.refresh_status()
    
    def update_adapter(self, adapter):
        """更新当前适配器（兼容性方法）"""
        self.set_current_adapter(adapter)
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.settings.get('remember_choice', False):
            # 如果记住选择，直接按照设置执行
            if self.settings.get('close_to_tray', True):
                event.ignore()
                self.hide()
            else:
                event.accept()
        else:
            # 显示确认对话框
            dialog = QMessageBox(self)
            dialog.setWindowTitle("关闭确认")
            dialog.setText("请选择关闭方式:")
            dialog.setIcon(QMessageBox.Question)
            
            # 添加自定义按钮
            minimize_btn = dialog.addButton("最小化到托盘", QMessageBox.AcceptRole)
            close_btn = dialog.addButton("完全退出", QMessageBox.RejectRole)
            cancel_btn = dialog.addButton("取消", QMessageBox.NoRole)
            
            # 添加记住选择的复选框
            remember_checkbox = QCheckBox("记住我的选择")
            dialog.setCheckBox(remember_checkbox)
            
            dialog.exec_()
            clicked_button = dialog.clickedButton()
            
            if clicked_button == minimize_btn:
                # 最小化到托盘
                if remember_checkbox.isChecked():
                    self.settings['close_to_tray'] = True
                    self.settings['remember_choice'] = True
                    self.save_settings()
                event.ignore()
                self.hide()
            elif clicked_button == close_btn:
                # 完全退出
                if remember_checkbox.isChecked():
                    self.settings['close_to_tray'] = False
                    self.settings['remember_choice'] = True
                    self.save_settings()
                event.accept()
                # 通知托盘应用退出
                if hasattr(self, 'tray_app'):
                    self.tray_app.quit_app()
            else:
                # 取消
                event.ignore()