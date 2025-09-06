# 网络配置切换工具 / Network Configuration Switcher

一个精致小巧的Python工具，用于快速切换网络配置。支持系统托盘图标，可通过右键菜单快速切换不同的网络环境设置。

A lightweight and elegant Python tool for quickly switching network configurations. Features system tray integration with right-click menu for seamless network environment switching.

**适用场景 / Use Cases：**
- 🏠 家庭网络：自动获取IP地址(DHCP) / Home Network: Automatic IP address (DHCP)
- 🏢 办公网络：固定IP地址配置 / Office Network: Static IP configuration
- 🌐 公共网络：快速切换DNS服务器 / Public Network: Quick DNS server switching
- 🔧 开发环境：多套网络配置快速切换 / Development Environment: Multiple network configuration switching

## 功能特性 / Features

### 核心功能 / Core Features
- 🌐 **多配置管理 / Multi-Configuration Management**：支持无限个网络配置模板 / Support unlimited network configuration templates
- 🔄 **一键切换 / One-Click Switching**：快速切换IP地址、子网掩码、网关和DNS设置 / Quick switching of IP address, subnet mask, gateway and DNS settings
- 📍 **系统托盘 / System Tray**：最小化后常驻后台，右键菜单快速操作 / Minimize to background with right-click menu for quick operations
- 🆕 **配置编辑 / Configuration Editing**：支持创建、编辑和删除自定义网络模板 / Support creating, editing and deleting custom network templates
- 🔧 **DHCP支持 / DHCP Support**：支持自动获取IP地址和静态IP配置 / Support automatic IP address acquisition and static IP configuration

### 技术特性 / Technical Features
- 🎯 **智能适配器检测 / Smart Adapter Detection**：自动识别可用网络适配器，过滤虚拟网卡 / Automatically identify available network adapters and filter virtual network cards
- 🔍 **实时状态监控 / Real-time Status Monitoring**：实时显示当前网络配置状态 / Real-time display of current network configuration status
- 💾 **配置持久化 / Configuration Persistence**：配置信息自动保存到本地文件 / Configuration information automatically saved to local files
- 🛡️ **权限管理 / Permission Management**：自动检测和请求管理员权限 / Automatically detect and request administrator privileges
- 🌍 **多语言支持 / Multi-language Support**：支持中英文系统环境 / Support Chinese and English system environments

## 安装依赖 / Installation

```bash
pip install -r requirements.txt
```

## 使用方法 / Usage

### 快速启动（推荐）/ Quick Start (Recommended)

**方法一：双击启动文件 / Method 1: Double-click Launch File**
- 双击 `启动网络配置工具.bat` 文件 / Double-click the `启动网络配置工具.bat` file
- 在弹出的UAC对话框中点击"是"授予管理员权限 / Click "Yes" in the UAC dialog to grant administrator privileges

**方法二：手动启动 / Method 2: Manual Launch**
1. 安装依赖项 / Install dependencies：
   ```bash
   pip install -r requirements.txt
   ```

2. 以管理员身份运行 / Run as administrator：
   - 右键点击 `main.py` 或 `run.bat` / Right-click `main.py` or `run.bat`
   - 选择"以管理员身份运行" / Select "Run as administrator"
   - 或在管理员权限的命令行中运行 / Or run in administrator command line：
     ```bash
     python main.py
     ```

### 程序使用 / Program Usage

1. **主界面操作 / Main Interface Operations**：
   - 程序启动后会自动显示主界面 / The main interface will be displayed automatically after startup
   - 在"选择适配器"下拉框中选择要配置的网卡 / Select the network adapter to configure in the "Select Adapter" dropdown
   - 查看当前网络状态和配置信息 / View current network status and configuration information

2. **配置管理 / Configuration Management**：
   - 应用配置：在配置模板列表中双击或点击"应用配置" / Apply Configuration: Double-click or click "Apply Configuration" in the template list
   - 新建配置：点击"新建配置"按钮 / New Configuration: Click the "New Configuration" button
   - 编辑配置：选择配置后点击"编辑配置" / Edit Configuration: Select a configuration and click "Edit Configuration"
   - 删除配置：选择配置后点击"删除配置" / Delete Configuration: Select a configuration and click "Delete Configuration"

3. **系统托盘 / System Tray**：
   - 右键点击托盘图标可快速切换配置 / Right-click the tray icon for quick configuration switching
   - 双击托盘图标打开主界面 / Double-click the tray icon to open the main interface
   - 关闭主界面时可选择最小化到托盘或完全退出 / Choose to minimize to tray or exit completely when closing the main interface

### 重要提示 / Important Notes

⚠️ **管理员权限必需 / Administrator Privileges Required**：修改网络配置需要管理员权限，请确保以管理员身份运行程序。/ Modifying network configuration requires administrator privileges. Please ensure the program runs as administrator.

💡 **首次使用 / First Use**：建议先创建几个常用的网络配置模板，如"家庭网络"、"办公网络"等。/ It is recommended to create several commonly used network configuration templates first, such as "Home Network", "Office Network", etc.

## 系统要求 / System Requirements

- **操作系统 / Operating System**：Windows 7/8/10/11
- **Python版本 / Python Version**：Python 3.6+
- **权限要求 / Permission Requirements**：管理员权限（修改网络配置必需）/ Administrator privileges (required for network configuration modification)
- **依赖库 / Dependencies**：详见 `requirements.txt` / See `requirements.txt`

## 故障排除 / Troubleshooting

### 常见问题 / Common Issues

**Q: 程序提示"需要管理员权限"？/ Program prompts "Administrator privileges required"?**
A: 右键点击程序文件，选择"以管理员身份运行"，或使用提供的 `启动网络配置工具.bat` 文件。/ Right-click the program file and select "Run as administrator", or use the provided `启动网络配置工具.bat` file.

**Q: 找不到网络适配器？/ Cannot find network adapters?**
A: 程序会自动过滤虚拟网卡，只显示可配置的物理网卡。如果仍然没有显示，请检查网卡驱动是否正常。/ The program automatically filters virtual network cards and only displays configurable physical network cards. If still not displayed, please check if the network card driver is working properly.

**Q: 配置切换失败？/ Configuration switching failed?**
A: 确保以管理员权限运行，并检查网络适配器是否正常工作。部分虚拟网卡可能不支持配置修改。/ Ensure running with administrator privileges and check if the network adapter is working properly. Some virtual network cards may not support configuration modification.

**Q: 托盘图标不显示？/ Tray icon not displayed?**
A: 检查系统托盘设置，确保允许程序在系统托盘显示图标。/ Check system tray settings to ensure the program is allowed to display icons in the system tray.

### 技术支持 / Technical Support

如遇到其他问题，请检查：/ If you encounter other issues, please check:
1. 是否以管理员权限运行 / Whether running with administrator privileges
2. Python环境和依赖是否正确安装 / Whether Python environment and dependencies are correctly installed
3. 网络适配器驱动是否正常 / Whether network adapter drivers are working properly
4. Windows防火墙或杀毒软件是否阻止程序运行 / Whether Windows firewall or antivirus software is blocking the program

## 默认配置示例 / Default Configuration Examples

程序内置以下示例配置：/ The program includes the following example configurations:
- **家庭网络 / Home Network**：192.168.124.233/255.255.255.0，网关 / Gateway：192.168.124.246，DNS：114.114.114.114
- **自动获取 / Automatic**：DHCP模式，自动获取IP地址和DNS服务器 / DHCP mode, automatically obtain IP address and DNS server

## 版本信息 / Version Information

**当前版本 / Current Version**：v1.0

**更新日志 / Changelog**：
- v1.0：初始版本发布 / Initial version release
  - 支持多网络配置管理 / Support multi-network configuration management
  - 系统托盘集成 / System tray integration
  - 智能适配器检测 / Smart adapter detection
  - 配置模板编辑功能 / Configuration template editing functionality

## 许可证 / License

本项目采用 MIT 许可证，详见 LICENSE 文件。/ This project is licensed under the MIT License - see the LICENSE file for details.

## 贡献 / Contributing

欢迎提交问题报告和功能请求！如果您想贡献代码，请先创建一个issue讨论您的想法。/ Welcome to submit issue reports and feature requests! If you want to contribute code, please create an issue first to discuss your ideas.

---

**开发者提示 / Developer Note**：本工具专为提高网络配置切换效率而设计，适合需要频繁切换网络环境的用户使用。/ This tool is designed to improve network configuration switching efficiency and is suitable for users who need to frequently switch network environments.
