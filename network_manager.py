import subprocess
import re
import json
import os
import ctypes
from typing import List, Dict, Optional

class NetworkAdapter:
    """网络适配器类"""
    def __init__(self, name: str, description: str, index: int):
        self.name = name
        self.description = description
        self.index = index
        self.current_config = None
    
    def __str__(self):
        return f"{self.description} ({self.name})"

class NetworkConfig:
    """网络配置类"""
    def __init__(self, name: str, ip: str = None, subnet: str = None, 
                 gateway: str = None, dns1: str = None, dns2: str = None, 
                 dhcp: bool = False):
        self.name = name
        self.ip = ip
        self.subnet = subnet
        self.gateway = gateway
        self.dns1 = dns1
        self.dns2 = dns2
        self.dhcp = dhcp
    
    def to_dict(self):
        return {
            'name': self.name,
            'ip': self.ip,
            'subnet': self.subnet,
            'gateway': self.gateway,
            'dns1': self.dns1,
            'dns2': self.dns2,
            'dhcp': self.dhcp
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class NetworkManager:
    """网络管理器"""
    
    def __init__(self):
        self.adapters = []
        self.configs = []
        self.config_file = 'network_configs.json'
        self.load_configs()
        self._load_default_configs()
    
    def _load_default_configs(self):
        """加载默认配置"""
        if not self.configs:
            # 添加默认的家庭网络配置
            home_config = NetworkConfig(
                name="家庭网络",
                ip="192.168.124.233",
                subnet="255.255.255.0",
                gateway="192.168.124.246",
                dns1="114.114.114.114",
                dns2="1.2.4.8"
            )
            
            # 添加DHCP配置
            dhcp_config = NetworkConfig(
                name="自动获取(DHCP)",
                dhcp=True
            )
            
            self.configs = [home_config, dhcp_config]
            self.save_configs()
    
    def get_network_adapters(self) -> List[NetworkAdapter]:
        """获取网络适配器列表（优先显示活跃的适配器，过滤无法获取配置的适配器）"""
        adapters = []
        active_adapters = []
        try:
            # 使用ipconfig命令获取适配器信息，尝试多种编码方式
            encodings = ['gbk', 'utf-8', 'cp936', 'gb2312']
            result = None
            
            for encoding in encodings:
                try:
                    result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True, encoding=encoding)
                    if result.returncode == 0:
                        print(f"成功使用编码 {encoding} 获取适配器信息")
                        break
                except UnicodeDecodeError:
                    print(f"编码 {encoding} 解码失败，尝试下一个")
                    continue
            
            if result is None or result.returncode != 0:
                print(f"获取适配器列表失败: {result.stderr if result else '所有编码尝试失败'}")
                return adapters
            
            # 解析ipconfig输出
            current_adapter = None
            current_description = None
            has_ip = False
            adapter_index = 1
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                # 检测适配器名称行（支持中英文格式）
                # 英文格式："Ethernet adapter 以太网:" 或 "Wireless LAN adapter WLAN 2:"
                # 中文格式："以太网适配器 以太网:" 或 "无线局域网适配器 WLAN 2:"
                if line and not line.startswith(' ') and line.endswith(':') and ('adapter' in line or '适配器' in line):
                    # 处理上一个适配器
                    if current_adapter and current_description:
                        self._process_adapter(current_adapter, current_description, has_ip, adapter_index, active_adapters, adapters)
                        adapter_index += 1
                    
                    # 提取适配器名称
                    adapter_name = None
                    if 'adapter ' in line:
                        # 英文格式："Ethernet adapter 以太网:"
                        adapter_name = line.split('adapter ')[1].rstrip(':')
                    elif '适配器 ' in line:
                        # 中文格式："以太网适配器 以太网:"
                        adapter_name = line.split('适配器 ')[1].rstrip(':')
                    
                    if adapter_name:
                        # 过滤一些不需要的适配器
                        skip_keywords = [
                            'Loopback', 'Teredo', 'ISATAP', 'Tunnel', 
                            '隧道', '环回', '本地连接* '
                        ]
                        
                        if not any(keyword in adapter_name for keyword in skip_keywords):
                            current_adapter = adapter_name
                            current_description = None
                            has_ip = False
                        else:
                            current_adapter = None
                    else:
                        current_adapter = None
                
                # 获取适配器描述
                elif current_adapter and (line.startswith('Description') or line.startswith('描述')):
                    current_description = line.split(':', 1)[1].strip() if ':' in line else ''
                
                # 检查是否有IP地址
                elif current_adapter and ('IPv4' in line or 'IP 地址' in line) and ':' in line:
                    ip_part = line.split(':', 1)[1].strip()
                    if ip_part and not ip_part.startswith('169.254') and ip_part != '0.0.0.0':
                        has_ip = True
            
            # 处理最后一个适配器
            if current_adapter and current_description:
                self._process_adapter(current_adapter, current_description, has_ip, adapter_index, active_adapters, adapters)
            
        except Exception as e:
            print(f"获取网络适配器失败: {e}")
        
        # 优先返回活跃的适配器，然后是其他可用适配器
        final_adapters = active_adapters + adapters
        print(f"最终适配器列表 (共{len(final_adapters)}个): {[str(a) for a in final_adapters]}")
        if active_adapters:
            print(f"活跃适配器 (共{len(active_adapters)}个): {[str(a) for a in active_adapters]}")
        
        self.adapters = final_adapters
        return final_adapters
    
    def _process_adapter(self, adapter_name: str, description: str, has_ip: bool, index: int, active_adapters: List[NetworkAdapter], adapters: List[NetworkAdapter]):
        """处理单个适配器"""
        # 进一步过滤虚拟适配器
        virtual_keywords = [
            'Microsoft', 'Teredo', 'ISATAP', 'Loopback',
            'WAN Miniport', 'Hyper-V', 'Virtual', 'Tailscale',
            'Tunnel', 'Wintun'
        ]
        
        # 检查是否为虚拟适配器
        is_virtual = any(keyword in description for keyword in virtual_keywords)
        
        if not is_virtual:
            print(f"检查适配器: {adapter_name} ({description})")
            
            # 降低过滤条件：只要有IP地址就认为是已连接的适配器
            if has_ip:
                adapter = NetworkAdapter(adapter_name, description, index)
                active_adapters.append(adapter)
                print(f"已连接适配器: {adapter_name}")
            else:
                # 对于没有IP的适配器，也添加到列表中但标记为未连接
                adapter = NetworkAdapter(adapter_name, description, index)
                adapters.append(adapter)
                print(f"未连接适配器: {adapter_name}")
    
    def get_current_config(self, adapter_name: str) -> Optional[Dict]:
        """获取当前网络配置"""
        try:
            # 获取IP配置，尝试多种编码方式
            cmd = f'netsh interface ip show config name="{adapter_name}"'
            encodings = ['gbk', 'utf-8', 'cp936', 'gb2312']
            result = None
            
            for encoding in encodings:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=encoding, errors='ignore')
                    if result.returncode == 0:
                        print(f"netsh命令成功，使用编码: {encoding}")
                        break
                except (UnicodeDecodeError, Exception) as e:
                    print(f"netsh命令编码 {encoding} 失败: {e}")
                    continue
            
            if result is None or result.returncode != 0:
                error_msg = result.stderr if result else "所有编码尝试失败"
                print(f"netsh命令失败 (返回码: {result.returncode if result else 'N/A'}): {error_msg}")
                print(f"尝试使用备选方案获取适配器 '{adapter_name}' 的配置")
                # 如果netsh命令失败，尝试使用ipconfig作为备选方案
                return self._get_config_fallback(adapter_name)
            
            output = result.stdout
            config = {}
            
            # 解析输出
            if "DHCP enabled:                         Yes" in output or "DHCP 已启用:                         是" in output:
                config['dhcp'] = True
            elif "DHCP enabled:                         No" in output or "DHCP 已启用:                         否" in output:
                config['dhcp'] = False
            else:
                # 如果无法确定DHCP状态，默认为False并尝试解析静态配置
                config['dhcp'] = False
            
            # 如果不是DHCP，解析静态IP配置
            if not config.get('dhcp', True):
                # 提取IP地址
                ip_match = re.search(r'IP Address:\s*([0-9.]+)', output)
                if not ip_match:
                    ip_match = re.search(r'IP 地址:\s*([0-9.]+)', output)
                if ip_match:
                    config['ip'] = ip_match.group(1)
                
                # 提取子网掩码
                subnet_match = re.search(r'Subnet Prefix:\s*[0-9.]+/(\d+)', output)
                if not subnet_match:
                    subnet_match = re.search(r'子网前缀长度:\s*(\d+)', output)
                if subnet_match:
                    prefix_length = int(subnet_match.group(1))
                    config['subnet'] = self._prefix_to_netmask(prefix_length)
                
                # 提取网关
                gateway_match = re.search(r'Default Gateway:\s*([0-9.]+)', output)
                if not gateway_match:
                    gateway_match = re.search(r'默认网关:\s*([0-9.]+)', output)
                if gateway_match:
                    config['gateway'] = gateway_match.group(1)
            
            # 从主输出中提取DNS配置（netsh ip show config已包含DNS信息）
            # 先尝试多行匹配获取完整的DNS部分
            dns_section = re.search(r'Statically Configured DNS Servers:[\s\S]*?(?=\n\s*[A-Z]|$)', output)
            if not dns_section:
                dns_section = re.search(r'静态配置的 DNS 服务器:[\s\S]*?(?=\n\s*[A-Z]|$)', output)
            
            dns_matches = []
            if dns_section:
                # 从DNS部分提取所有IP地址
                dns_matches = re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', dns_section.group())
            
            if dns_matches:
                config['dns1'] = dns_matches[0] if len(dns_matches) > 0 else None
                config['dns2'] = dns_matches[1] if len(dns_matches) > 1 else None
            
            return config
            
        except Exception as e:
            print(f"获取当前配置失败: {e}")
            return None
    
    def _get_config_fallback(self, adapter_name: str) -> Optional[Dict]:
        """备选方案：使用ipconfig获取网络配置"""
        try:
            print(f"使用ipconfig备选方案获取适配器 '{adapter_name}' 的配置")
            # 使用ipconfig /all获取详细信息，尝试多种编码
            encodings = ['gbk', 'utf-8', 'cp936', 'gb2312']
            result = None
            
            for encoding in encodings:
                try:
                    result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True, encoding=encoding)
                    if result.returncode == 0:
                        print(f"ipconfig备选方案成功，使用编码: {encoding}")
                        break
                except UnicodeDecodeError:
                    print(f"ipconfig备选方案编码 {encoding} 解码失败")
                    continue
            
            if result is None or result.returncode != 0:
                error_msg = result.stderr if result else "所有编码尝试失败"
                print(f"ipconfig命令执行失败 (返回码: {result.returncode if result else 'N/A'}): {error_msg}")
                return None
            
            output = result.stdout
            config = {}
            
            # 查找指定适配器的配置段
            adapter_section = None
            lines = output.split('\n')
            # 开始查找适配器配置段
            
            for i, line in enumerate(lines):
                # 检查适配器标题行（不以空格开头的行且包含'适配器'或以':'结尾）
                if (not line.startswith(' ') and line.strip() and 
                    ('适配器' in line or line.strip().endswith(':'))):
                    # 检查适配器标题行
                    
                    # 收集这个适配器的配置段
                    temp_section = []
                    j = i + 1
                    while j < len(lines) and (not lines[j].strip() or lines[j].startswith(' ')):
                        temp_section.append(lines[j])
                        j += 1
                        # 如果遇到下一个适配器标题行，停止
                        if j < len(lines) and lines[j].strip() and not lines[j].startswith(' '):
                            break
                    
                    # 检查这个适配器段是否包含目标描述
                    temp_text = '\n'.join(temp_section)
                    # 支持中英文描述格式
                    description_line_cn = f'描述. . . . . . . . . . . . . . . : {adapter_name}'
                    description_line_en = f'Description . . . . . . . . . . . : {adapter_name}'
                    
                    if description_line_cn in temp_text or description_line_en in temp_text:
                        adapter_section = temp_section
                        # 通过描述匹配找到适配器
                        break
                    else:
                        # 继续查找下一个适配器
                        pass
            
            # 如果没找到指定适配器，尝试使用第一个有IPv4地址的适配器
            if not adapter_section:
                # 未找到指定适配器，尝试使用第一个有IPv4地址的适配器
                for i, line in enumerate(lines):
                    if ('以太网适配器' in line or '无线局域网适配器' in line or '隧道适配器' in line):
                        # 检查这个适配器是否有IPv4地址
                        temp_section = []
                        j = i + 1
                        while j < len(lines) and not (lines[j].strip() and not lines[j].startswith(' ')):
                            temp_section.append(lines[j])
                            j += 1
                        
                        # 检查是否包含IPv4地址和目标适配器描述
                        temp_text = '\n'.join(temp_section)
                        if 'IPv4 地址' in temp_text:
                            # 检查描述是否匹配
                            if f'描述. . . . . . . . . . . . . . . : {adapter_name}' in temp_text:
                                adapter_section = temp_section
                                print(f"通过IPv4地址和描述匹配找到适配器: {line.strip()}")
                                break
                            # 如果没有找到精确匹配，使用第一个有IPv4的适配器作为备选
                            elif not adapter_section:
                                adapter_section = temp_section
                                print(f"使用备选适配器: {line.strip()}")
            
            if not adapter_section:
                # 未找到适配器配置信息
                # 显示可用的适配器列表
                for line in lines:
                    if '适配器' in line and line.strip():
                        print(f"  - {line.strip()}")
                return None
            
            adapter_text = '\n'.join(adapter_section)
            
            # 检查DHCP状态 - 支持中英文
            if ('DHCP 已启用' in adapter_text or 'DHCP Enabled' in adapter_text or
                'DHCP enabled' in adapter_text):
                config['dhcp'] = True
            else:
                config['dhcp'] = False
            
            # 提取IP地址 - 支持中英文格式
            ip_match = re.search(r'IPv4 地址[^:]*:\s*([0-9.]+)', adapter_text)
            if not ip_match:
                ip_match = re.search(r'IPv4 Address[^:]*:\s*([0-9.]+)', adapter_text)
            if not ip_match:
                ip_match = re.search(r'IP Address[^:]*:\s*([0-9.]+)', adapter_text)
            if ip_match:
                config['ip'] = ip_match.group(1)
            
            # 提取子网掩码 - 支持中英文格式
            subnet_match = re.search(r'子网掩码[^:]*:\s*([0-9.]+)', adapter_text)
            if not subnet_match:
                subnet_match = re.search(r'Subnet Mask[^:]*:\s*([0-9.]+)', adapter_text)
            if subnet_match:
                config['subnet'] = subnet_match.group(1)
            
            # 提取默认网关 - 支持中英文格式和多行格式
            gateway_match = re.search(r'默认网关[^:]*:[^\n]*\n?[^\n]*?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', adapter_text, re.MULTILINE)
            if not gateway_match:
                gateway_match = re.search(r'Default Gateway[^:]*:[^\n]*\n?[^\n]*?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', adapter_text, re.MULTILINE)
            if not gateway_match:
                gateway_match = re.search(r'默认网关[^:]*:\s*([0-9.]+)', adapter_text)
            if not gateway_match:
                gateway_match = re.search(r'Default Gateway[^:]*:\s*([0-9.]+)', adapter_text)
            if not gateway_match:
                gateway_match = re.search(r'网关[^:]*:\s*([0-9.]+)', adapter_text)
            if gateway_match:
                config['gateway'] = gateway_match.group(1)
            
            # 提取DNS服务器 - 支持中英文格式和多行格式
            dns_matches = re.findall(r'DNS 服务器[^:]*:[^\n]*\n?[^\n]*?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', adapter_text, re.MULTILINE)
            if not dns_matches:
                dns_matches = re.findall(r'DNS Servers[^:]*:[^\n]*\n?[^\n]*?([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', adapter_text, re.MULTILINE)
            if not dns_matches:
                dns_matches = re.findall(r'DNS 服务器[^:]*:\s*([0-9.]+)', adapter_text)
            if not dns_matches:
                dns_matches = re.findall(r'DNS Servers[^:]*:\s*([0-9.]+)', adapter_text)
            if not dns_matches:
                dns_matches = re.findall(r'DNS[^:]*:\s*([0-9.]+)', adapter_text)
            if dns_matches:
                config['dns1'] = dns_matches[0] if len(dns_matches) > 0 else None
                config['dns2'] = dns_matches[1] if len(dns_matches) > 1 else None
            
            # 检查是否解析到了有效的配置信息
            if config and ('ip' in config or 'dhcp' in config):
                return config
            else:
                return None
            
        except Exception as e:
            print(f"备选方案获取配置失败: {e}")
            return None
    
    def _get_interface_names(self) -> List[str]:
        """获取netsh接口名称列表"""
        try:
            cmd = 'netsh interface show interface'
            
            # 尝试不同的编码方式
            encodings = ['utf-8', 'gbk', 'cp936', 'latin1']
            result = None
            
            for encoding in encodings:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=encoding)
                    if result.returncode == 0 and result.stdout:
                        break
                except UnicodeDecodeError:
                    continue
            
            if not result or result.returncode != 0:
                print(f"获取接口列表失败")
                return []
            
            interface_names = []
            lines = result.stdout.strip().split('\n')
            
            for line in lines[3:]:  # 跳过标题行
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        # 接口名称是最后一部分，可能包含空格
                        interface_name = ' '.join(parts[3:])
                        interface_names.append(interface_name)
            
            return interface_names
            
        except Exception as e:
            print(f"获取接口名称失败: {e}")
            return []
    
    def _get_connection_name(self, adapter_name: str) -> Optional[str]:
        """根据适配器名称获取netsh可识别的连接名称"""
        try:
            # 首先尝试直接使用适配器名称
            test_cmd = f'netsh interface ip show config name="{adapter_name}"'
            result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return adapter_name
            
            # 获取所有可用的连接名称
            interface_names = self._get_interface_names()
            
            # 尝试模糊匹配
            adapter_lower = adapter_name.lower()
            for interface_name in interface_names:
                interface_lower = interface_name.lower()
                # 检查是否包含关键词
                if (adapter_lower in interface_lower or 
                    interface_lower in adapter_lower or
                    any(word in interface_lower for word in adapter_lower.split()) or
                    any(word in adapter_lower for word in interface_lower.split())):
                    return interface_name
            
            # 如果没有找到匹配，返回None
            return None
            
        except Exception as e:
            print(f"获取连接名称失败: {e}")
            return None
    
    def _prefix_to_netmask(self, prefix_length: int) -> str:
        """将前缀长度转换为子网掩码"""
        mask_map = {
            8: "255.0.0.0",
            16: "255.255.0.0",
            24: "255.255.255.0",
            25: "255.255.255.128",
            26: "255.255.255.192",
            27: "255.255.255.224",
            28: "255.255.255.240",
            29: "255.255.255.248",
            30: "255.255.255.252"
        }
        return mask_map.get(prefix_length, "255.255.255.0")
    
    def _is_admin(self) -> bool:
        """检查是否有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def apply_config(self, adapter_name: str, config: NetworkConfig) -> bool:
        """应用网络配置"""
        try:
            # 检查管理员权限
            if not self._is_admin():
                print("错误：需要管理员权限才能修改网络配置")
                return False
            
            # 获取netsh可识别的连接名称
            connection_name = self._get_connection_name(adapter_name)
            if not connection_name:
                print(f"无法找到适配器 '{adapter_name}' 对应的连接名称")
                return False
            
            if config.dhcp:
                # 设置为DHCP
                ip_cmd = f'netsh interface ip set address name="{connection_name}" dhcp'
                dns_cmd = f'netsh interface ip set dns name="{connection_name}" dhcp'
            else:
                # 设置静态IP
                ip_cmd = f'netsh interface ip set address name="{connection_name}" static {config.ip} {config.subnet}'
                if config.gateway:
                    ip_cmd += f' {config.gateway}'
                
                # 设置DNS
                if config.dns1:
                    dns_cmd = f'netsh interface ip set dns name="{connection_name}" static {config.dns1}'
                    if config.dns2:
                        dns_cmd += f' && netsh interface ip add dns name="{connection_name}" {config.dns2} index=2'
                else:
                    dns_cmd = f'netsh interface ip set dns name="{connection_name}" dhcp'
            
            print(f"正在应用配置到适配器: {adapter_name} (连接名称: {connection_name})")
            
            # 执行IP配置命令
            ip_result = subprocess.run(ip_cmd, shell=True, capture_output=True, text=True, encoding='gbk')
            if ip_result.returncode != 0:
                error_msg = ip_result.stderr or ip_result.stdout
                print(f"设置IP失败: {error_msg}")
                return False
            
            # 执行DNS配置命令
            dns_result = subprocess.run(dns_cmd, shell=True, capture_output=True, text=True, encoding='gbk')
            if dns_result.returncode != 0:
                error_msg = dns_result.stderr or dns_result.stdout
                print(f"设置DNS失败: {error_msg}")
                return False
            
            print("网络配置应用成功")
            return True
            
        except Exception as e:
            print(f"应用配置失败: {e}")
            return False
    
    def save_configs(self):
        """保存配置到文件"""
        try:
            data = [config.to_dict() for config in self.configs]
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def load_configs(self):
        """从文件加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.configs = [NetworkConfig.from_dict(item) for item in data]
            else:
                self.configs = []
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.configs = []
    
    def add_config(self, config: NetworkConfig):
        """添加新配置"""
        self.configs.append(config)
        self.save_configs()
    
    def remove_config(self, config_name: str):
        """删除配置"""
        self.configs = [c for c in self.configs if c.name != config_name]
        self.save_configs()
    
    def get_config_by_name(self, name: str) -> Optional[NetworkConfig]:
        """根据名称获取配置"""
        for config in self.configs:
            if config.name == name:
                return config
        return None