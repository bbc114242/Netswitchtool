# 网络配置切换工具

一个精致小巧的Python工具，用于快速切换网络配置。支持系统托盘图标，可通过右键菜单快速切换不同的网络环境设置。

**适用场景：**
- 🏠 家庭网络：自动获取IP地址(DHCP)
- 🏢 办公网络：固定IP地址配置
- 🌐 公共网络：快速切换DNS服务器
- 🔧 开发环境：多套网络配置快速切换

## 功能特性

### 核心功能
- 🌐 **多配置管理**：支持无限个网络配置模板
- 🔄 **一键切换**：快速切换IP地址、子网掩码、网关和DNS设置
- 📍 **系统托盘**：最小化后常驻后台，右键菜单快速操作
- 🆕 **配置编辑**：支持创建、编辑和删除自定义网络模板
- 🔧 **DHCP支持**：支持自动获取IP地址和静态IP配置

### 技术特性
- 🎯 **智能适配器检测**：自动识别可用网络适配器，过滤虚拟网卡
- 🔍 **实时状态监控**：实时显示当前网络配置状态
- 💾 **配置持久化**：配置信息自动保存到本地文件
- 🛡️ **权限管理**：自动检测和请求管理员权限
- 🌍 **多语言支持**：支持中英文系统环境

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 快速启动（推荐）

**方法一：双击启动文件**
- 双击 `启动网络配置工具.bat` 文件
- 在弹出的UAC对话框中点击"是"授予管理员权限

**方法二：手动启动**
1. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

2. 以管理员身份运行：
   - 右键点击 `main.py` 或 `run.bat`
   - 选择"以管理员身份运行"
   - 或在管理员权限的命令行中运行：
     ```bash
     python main.py
     ```

### 程序使用

1. **主界面操作**：
   - 程序启动后会自动显示主界面
   - 在"选择适配器"下拉框中选择要配置的网卡
   - 查看当前网络状态和配置信息

2. **配置管理**：
   - 应用配置：在配置模板列表中双击或点击"应用配置"
   - 新建配置：点击"新建配置"按钮
   - 编辑配置：选择配置后点击"编辑配置"
   - 删除配置：选择配置后点击"删除配置"

3. **系统托盘**：
   - 右键点击托盘图标可快速切换配置
   - 双击托盘图标打开主界面
   - 关闭主界面时可选择最小化到托盘或完全退出

### 重要提示

⚠️ **管理员权限必需**：修改网络配置需要管理员权限，请确保以管理员身份运行程序。

💡 **首次使用**：建议先创建几个常用的网络配置模板，如"家庭网络"、"办公网络"等。

## 系统要求

- **操作系统**：Windows 7/8/10/11
- **Python版本**：Python 3.6+
- **权限要求**：管理员权限（修改网络配置必需）
- **依赖库**：详见 `requirements.txt`

## 故障排除

### 常见问题

**Q: 程序提示"需要管理员权限"？**
A: 右键点击程序文件，选择"以管理员身份运行"，或使用提供的 `启动网络配置工具.bat` 文件。

**Q: 找不到网络适配器？**
A: 程序会自动过滤虚拟网卡，只显示可配置的物理网卡。如果仍然没有显示，请检查网卡驱动是否正常。

**Q: 配置切换失败？**
A: 确保以管理员权限运行，并检查网络适配器是否正常工作。部分虚拟网卡可能不支持配置修改。

**Q: 托盘图标不显示？**
A: 检查系统托盘设置，确保允许程序在系统托盘显示图标。

### 技术支持

如遇到其他问题，请检查：
1. 是否以管理员权限运行
2. Python环境和依赖是否正确安装
3. 网络适配器驱动是否正常
4. Windows防火墙或杀毒软件是否阻止程序运行

## 默认配置示例

程序内置以下示例配置：
- **家庭网络**：192.168.124.233/255.255.255.0，网关：192.168.124.246，DNS：114.114.114.114
- **自动获取**：DHCP模式，自动获取IP地址和DNS服务器

## 版本信息

**当前版本**：v1.0

**更新日志**：
- v1.0：初始版本发布
  - 支持多网络配置管理
  - 系统托盘集成
  - 智能适配器检测
  - 配置模板编辑功能

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交问题报告和功能请求！如果您想贡献代码，请先创建一个issue讨论您的想法。

---

**开发者提示**：本工具专为提高网络配置切换效率而设计，适合需要频繁切换网络环境的用户使用。

---

# Network Configuration Switcher

A lightweight and elegant Python tool for quickly switching network configurations. Features system tray integration with right-click menu for seamless network environment switching.

**Use Cases:**
- 🏠 Home Network: Automatic IP address (DHCP)
- 🏢 Office Network: Static IP configuration
- 🌐 Public Network: Quick DNS server switching
- 🔧 Development Environment: Multiple network configuration switching

## Features

### Core Features
- 🌐 **Multi-Configuration Management**: Support unlimited network configuration templates
- 🔄 **One-Click Switching**: Quick switching of IP address, subnet mask, gateway and DNS settings
- 📍 **System Tray**: Minimize to background with right-click menu for quick operations
- 🆕 **Configuration Editing**: Support creating, editing and deleting custom network templates
- 🔧 **DHCP Support**: Support automatic IP address acquisition and static IP configuration

### Technical Features
- 🎯 **Smart Adapter Detection**: Automatically identify available network adapters and filter virtual network cards
- 🔍 **Real-time Status Monitoring**: Real-time display of current network configuration status
- 💾 **Configuration Persistence**: Configuration information automatically saved to local files
- 🛡️ **Permission Management**: Automatically detect and request administrator privileges
- 🌍 **Multi-language Support**: Support Chinese and English system environments

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Recommended)

**Method 1: Double-click Launch File**
- Double-click the `启动网络配置工具.bat` file
- Click "Yes" in the UAC dialog to grant administrator privileges

**Method 2: Manual Launch**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run as administrator:
   - Right-click `main.py` or `run.bat`
   - Select "Run as administrator"
   - Or run in administrator command line:
     ```bash
     python main.py
     ```

### Program Usage

1. **Main Interface Operations**:
   - The main interface will be displayed automatically after startup
   - Select the network adapter to configure in the "Select Adapter" dropdown
   - View current network status and configuration information

2. **Configuration Management**:
   - Apply Configuration: Double-click or click "Apply Configuration" in the template list
   - New Configuration: Click the "New Configuration" button
   - Edit Configuration: Select a configuration and click "Edit Configuration"
   - Delete Configuration: Select a configuration and click "Delete Configuration"

3. **System Tray**:
   - Right-click the tray icon for quick configuration switching
   - Double-click the tray icon to open the main interface
   - Choose to minimize to tray or exit completely when closing the main interface

### Important Notes

⚠️ **Administrator Privileges Required**: Modifying network configuration requires administrator privileges. Please ensure the program runs as administrator.

💡 **First Use**: It is recommended to create several commonly used network configuration templates first, such as "Home Network", "Office Network", etc.

## System Requirements

- **Operating System**: Windows 7/8/10/11
- **Python Version**: Python 3.6+
- **Permission Requirements**: Administrator privileges (required for network configuration modification)
- **Dependencies**: See `requirements.txt`

## Troubleshooting

### Common Issues

**Q: Program prompts "Administrator privileges required"?**
A: Right-click the program file and select "Run as administrator", or use the provided `启动网络配置工具.bat` file.

**Q: Cannot find network adapters?**
A: The program automatically filters virtual network cards and only displays configurable physical network cards. If still not displayed, please check if the network card driver is working properly.

**Q: Configuration switching failed?**
A: Ensure running with administrator privileges and check if the network adapter is working properly. Some virtual network cards may not support configuration modification.

**Q: Tray icon not displayed?**
A: Check system tray settings to ensure the program is allowed to display icons in the system tray.

### Technical Support

If you encounter other issues, please check:
1. Whether running with administrator privileges
2. Whether Python environment and dependencies are correctly installed
3. Whether network adapter drivers are working properly
4. Whether Windows firewall or antivirus software is blocking the program

## Default Configuration Examples

The program includes the following example configurations:
- **Home Network**: 192.168.124.233/255.255.255.0, Gateway: 192.168.124.246, DNS: 114.114.114.114
- **Automatic**: DHCP mode, automatically obtain IP address and DNS server

## Version Information

**Current Version**: v1.0

**Changelog**:
- v1.0: Initial version release
  - Support multi-network configuration management
  - System tray integration
  - Smart adapter detection
  - Configuration template editing functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Welcome to submit issue reports and feature requests! If you want to contribute code, please create an issue first to discuss your ideas.

---

**Developer Note**: This tool is designed to improve network configuration switching efficiency and is suitable for users who need to frequently switch network environments.
