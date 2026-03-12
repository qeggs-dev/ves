# VES - Virtual Environment System

VES 是一个用于简化 Python 虚拟环境管理的工具，用于快速启动 REPL、执行脚本和进入交互式 Shell。
它能够像使用命令一样管理多个虚拟环境，快速的切换和运行代码。

## 核心用途

- **快速启动 REPL**：在指定虚拟环境中启动 Python 交互式解释器
- **执行脚本**：在虚拟环境中运行 Python 脚本文件
- **进入 Shell**：激活虚拟环境的命令行环境
- **批量命令执行**：通过脚本文件自动化环境操作

## 功能特性

- 创建、删除、列出虚拟环境
- 在环境中安装/卸载包
- 从 `requirements.txt` 安装依赖
- 冻结环境包列表
- 复制已有环境
- 一键进入环境 Shell 或 REPL
- 支持变量管理和条件跳转（用于自动化脚本）
- 支持从文件批量执行命令
- 跨平台支持（Windows、Linux、macOS）

## 安装

VES 无需安装，克隆或下载项目即可使用，需要 Python 3.8+。

```bash
git clone https://github.com/your-repo/ves.git
cd ves
```

## 快速开始

### 启动 REPL

在指定虚拟环境中启动 Python REPL：

```bash
python ves.py repl myenv
```

### 执行 Python 脚本

在虚拟环境中运行脚本：

```bash
python ves.py exec myenv script.py
```

### 进入环境 Shell

激活虚拟环境的命令行环境：

```bash
python ves.py shell myenv
```

### 交互式模式

直接运行进入交互式命令行：

```bash
python ves.py
```

然后在提示符下输入命令：

```
> create myenv
> install myenv requests
> repl myenv
```

## 命令详解

#### 环境操作

| 命令 | 描述 |
|------|------|
| `create <env_name>` | 创建虚拟环境 |
| `remove <env_name>` | 删除虚拟环境 |
| `list` | 列出所有环境 |
| `copy <src_env> <dst_env>` | 复制环境 |

#### 包管理

| 命令 | 描述 |
|------|------|
| `install <env_name> <package>` | 安装包 |
| `uninstall <env_name> <package>` | 卸载包 |
| `ifr <env_name> <requirements_file>` | 从 requirements 文件安装 |
| `freeze <env_name> [output_file]` | 冻结当前包列表 |

#### 运行环境

| 命令 | 描述 |
|------|------|
| `repl <env_name>` | 进入环境 Python REPL |
| `shell <env_name>` | 进入环境 Shell |
| `exec <env_name> <script_path>` | 在环境中执行 Python 脚本 |

#### 脚本控制

| 命令 | 描述 |
|------|------|
| `set_var <key> <value>` | 设置变量 |
| `set_const <key> <value>` | 设置常量（只读） |
| `get_var <key>` | 获取变量值 |
| `jump <line> [absolute]` | 跳转到指定行（仅文件模式） |
| `je/jne/jlt/jgt/jle/jge` | 条件比较跳转 |
| `jt/jf <key> <line>` | 根据变量真假跳转 |

#### 其他

| 命令 | 描述 |
|------|------|
| `print <...>` | 打印内容 |
| `title <title>` | 设置控制台标题 |
| `execute <file_path>` | 执行 VES 脚本文件 |
| `cmdls [json_format]` | 列出所有命令 |
| `help` | 显示帮助信息 |
| `exit [code]` | 退出 CLI |

## 使用场景示例

### 场景1：快速测试环境

```bash
# 创建临时环境并进入 REPL
python ves.py create testenv
python ves.py repl testenv
```

### 场景2：运行项目脚本

```bash
# 在项目环境中运行初始化脚本
python ves.py exec projectenv ./scripts/init.py
```

### 场景3：自动化环境设置（使用脚本文件）

创建 `setup.ves`：

```
create project
install project flask
install project requests
freeze project requirements.txt
repl project
```

执行：

```bash
python ves.py execute setup.ves
```

## 变量与脚本控制

VES 脚本支持变量和条件跳转，适用于自动化任务：

```
set_var env_name "myapp"
create $env_name
install $env_name flask
install $env_name pytest
jump 5
print "安装完成"
```

变量引用使用 `$` 符号。

## 平台支持说明

- **Windows**：使用 PowerShell 激活环境
- **Linux/macOS**：使用 Bash 激活环境

## 许可证

[MIT License](LICENSE)