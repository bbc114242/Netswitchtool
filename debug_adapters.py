#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from network_manager import NetworkManager

def test_ipconfig():
    """测试ipconfig命令输出"""
    print("=== 测试ipconfig命令 ===")
    try:
        encodings = ['gbk', 'utf-8', 'cp936', 'gb2312']
        for encoding in encodings:
            try:
                result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True, encoding=encoding)
                if result.returncode == 0:
                    print(f"✓ 编码 {encoding} 成功")
                    lines = result.stdout.split('\n')[:20]  # 只显示前20行
                    for i, line in enumerate(lines):
                        print(f"{i+1:2d}: {line}")
                    break
                else:
                    print(f"✗ 编码 {encoding} 失败: {result.stderr}")
            except UnicodeDecodeError as e:
                print(f"✗ 编码 {encoding} 解码错误: {e}")
    except Exception as e:
        print(f"✗ ipconfig命令执行失败: {e}")

def test_network_manager():
    """测试NetworkManager"""
    print("\n=== 测试NetworkManager ===")
    try:
        nm = NetworkManager()
        print("✓ NetworkManager初始化成功")
        
        print("\n--- 获取网络适配器 ---")
        adapters = nm.get_network_adapters()
        print(f"找到 {len(adapters)} 个适配器:")
        
        for i, adapter in enumerate(adapters):
            print(f"{i+1}. {adapter.name} - {adapter.description}")
            
            # 测试获取当前配置
            config = nm.get_current_config(adapter.name)
            if config:
                print(f"   配置: IP={config.get('ip', 'N/A')}, DHCP={config.get('dhcp', 'N/A')}")
            else:
                print("   配置: 无法获取")
                
    except Exception as e:
        print(f"✗ NetworkManager测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_netsh():
    """测试netsh命令"""
    print("\n=== 测试netsh命令 ===")
    try:
        result = subprocess.run('netsh interface show interface', shell=True, capture_output=True, text=True, encoding='gbk')
        if result.returncode == 0:
            print("✓ netsh interface命令成功")
            print(result.stdout[:500])  # 显示前500字符
        else:
            print(f"✗ netsh interface命令失败: {result.stderr}")
    except Exception as e:
        print(f"✗ netsh命令执行失败: {e}")

if __name__ == "__main__":
    print("网络适配器调试工具")
    print("=" * 50)
    
    test_ipconfig()
    test_netsh()
    test_network_manager()
    
    print("\n=== 调试完成 ===")
    input("按回车键退出...")