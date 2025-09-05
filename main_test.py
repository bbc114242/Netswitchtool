#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络配置管理工具 - 测试版本
主程序入口（跳过管理员权限检查用于测试）
"""

import sys
import os
import ctypes
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from network_manager import NetworkManager
from system_tray import SystemTrayApp

def check_dependencies():
    """检查必要的依赖项"""
    try:
        import PyQt5
        import subprocess
        import json
        return True
    except ImportError as e:
        print(f"缺少必要的依赖项: {e}")
        print("请运行: pip install PyQt5")
        return False

def is_admin():
    """检查是否具有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员身份重新运行程序"""
    try:
        if sys.argv[-1] != 'asadmin':
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            return True
    except Exception as e:
        print(f"无法获取管理员权限: {e}")
        return False
    return False

def main():
    """主程序入口 - 测试版本"""
    try:
        # 检查依赖项
        if not check_dependencies():
            print("依赖项检查失败，程序无法启动")
            input("按任意键退出...")
            return
        
        # 测试版本：跳过管理员权限检查
        print("测试模式：跳过管理员权限检查")
        print("注意：在测试模式下可能无法实际修改网络配置")
        
        # 创建应用程序
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)  # 关闭窗口时不退出程序
        
        # 创建网络管理器
        network_manager = NetworkManager()
        
        # 创建系统托盘应用（会自动显示主界面）
        tray_app = SystemTrayApp(network_manager)
        
        # 运行应用
        sys.exit(app.exec_())
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按任意键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()