#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络配置切换工具
一个精致小巧的Python工具，用于快速切换网络配置
"""

import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from system_tray import SystemTrayApp
from network_manager import NetworkManager

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        print("正在检查管理员权限...")
        # 使用更安全的方式检查管理员权限
        import threading
        import time
        
        result = [False]  # 使用列表来存储结果，避免闭包问题
        exception_occurred = [False]
        
        def check_admin():
            try:
                result[0] = ctypes.windll.shell32.IsUserAnAdmin() != 0
                print(f"管理员权限检查结果: {result[0]}")
            except Exception as e:
                print(f"检查管理员权限时出错: {e}")
                exception_occurred[0] = True
                result[0] = False
        
        # 创建线程执行权限检查，设置超时
        thread = threading.Thread(target=check_admin)
        thread.daemon = True
        thread.start()
        thread.join(timeout=5)  # 5秒超时
        
        if thread.is_alive():
            print("管理员权限检查超时，假设没有管理员权限")
            return False
        
        if exception_occurred[0]:
            return False
            
        return result[0]
    except Exception as e:
        print(f"检查管理员权限时出错: {e}")
        return False

def run_as_admin():
    """以管理员权限重新运行程序"""
    try:
        if sys.argv[-1] != 'asadmin':
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            return True
    except Exception as e:
        print(f"请求管理员权限失败: {e}")
        return False
    return False

def check_dependencies():
    """检查依赖项"""
    missing_deps = []
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append('PyQt5')
    
    try:
        import psutil
    except ImportError:
        missing_deps.append('psutil')
    
    try:
        import win32api
    except ImportError:
        missing_deps.append('pywin32')
    
    if missing_deps:
        error_msg = f"缺少以下依赖项:\n{', '.join(missing_deps)}\n\n请运行以下命令安装:\npip install -r requirements.txt"
        if 'PyQt5' not in missing_deps:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "依赖项错误", error_msg)
        else:
            print(error_msg)
        return False
    
    return True

class NetworkSwitcherApp:
    """网络切换应用主类"""
    
    def __init__(self):
        print("初始化NetworkManager...")
        self.network_manager = NetworkManager()
        print("初始化ConfigManager...")
        self.config_manager = ConfigManager()
        print("初始化完成，准备创建系统托盘...")
        self.tray_app = None

def main():
    """主程序入口"""
    try:
        # 检查管理员权限
        if not is_admin():
            error_msg = "错误：需要管理员权限来修改网络配置\n\n解决方案：\n1. 右键点击程序，选择'以管理员身份运行'\n2. 或者双击'启动网络配置工具.bat'文件\n3. 在弹出的UAC对话框中点击'是'"
            try:
                app = QApplication(sys.argv)
                QMessageBox.critical(None, "权限错误", error_msg)
            except:
                print(error_msg)
            return 1
        
        # 检查依赖项
        if not check_dependencies():
            error_msg = "依赖项检查失败，程序无法启动"
            try:
                app = QApplication(sys.argv)
                QMessageBox.critical(None, "依赖项错误", error_msg)
            except:
                print(error_msg)
            return
        
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
        return 0
    except Exception as e:
        error_msg = f"程序运行时发生错误: {str(e)}"
        print(error_msg)
        
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "运行错误", error_msg)
        except:
            pass
        
        return 1

if __name__ == "__main__":
    try:
        print("程序启动中...")
        print("检查管理员权限...")
        exit_code = main()
        print(f"程序退出，退出码: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        print(f"程序运行时发生错误: {str(e)}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        # 显示错误对话框
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "错误", f"程序运行时发生错误: {str(e)}")
        except:
            pass
        input("按回车键退出...")  # 保持控制台窗口打开
        sys.exit(1)