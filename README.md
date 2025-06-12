# MCP Weather Project 🌤️

一个基于 Model Context Protocol (MCP) 的天气查询系统，包含天气服务器和智能客户端。

## 📋 项目概述

本项目实现了一个完整的 MCP 生态系统，包括：

- **Weather Server** (`server/`): 基于美国国家气象局 (NWS) API 的天气服务器
- **MCP Client** (`mcp-client/`): 支持 DeepSeek V3 API 的智能客户端

## 🏗️ 项目结构

```
mcp/
├── server/                    # 天气服务器
│   ├── weather.py            # 主服务器文件
│   ├── pyproject.toml        # 服务器依赖配置
│   └── README.md             # 服务器说明文档
├── mcp-client/               # MCP 客户端
│   ├── client.py             # 主客户端文件
│   ├── pyproject.toml        # 客户端依赖配置
│   └── README.md             # 客户端说明文档
├── .gitignore
├── LICENSE
└── README.md                 # 项目主说明文档
```

## ⚡ 功能特性

### Weather Server 功能

- 🌡️ **天气预报查询**: 根据经纬度获取详细天气预报
- ⚠️ **天气警报查询**: 获取美国各州的天气警报信息
- 🔄 **异步处理**: 高效的异步 HTTP 请求处理
- 🛡️ **错误处理**: 完善的异常处理和错误恢复机制

### MCP Client 功能

- 🤖 **AI 驱动**: 集成 DeepSeek V3 API 进行智能对话
- 🔧 **工具调用**: 自动识别并调用 MCP 服务器提供的工具
- 💬 **交互式聊天**: 支持持续对话和上下文理解
- 🔌 **多语言支持**: 支持 Python 和 JavaScript MCP 服务器

## 🚀 快速开始

### 环境要求

- Python 3.11+
- uv (推荐的包管理器)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd mcp
   ```

2. **安装服务器依赖**
   ```bash
   cd server
   uv sync
   ```

3. **安装客户端依赖**
   ```bash
   cd ../mcp-client
   uv sync
   ```

4. **配置环境变量**
   
   在 `mcp-client/` 目录下创建 `.env` 文件：
   ```env
   API_KEY=your_deepseek_api_key
   BASE_URL=https://api.deepseek.com
   MODEL=deepseek-chat
   ```

### 运行项目

1. **启动天气服务器**
   ```bash
   cd server
   python weather.py
   ```

2. **启动客户端**
   ```bash
   cd mcp-client
   python client.py ../server/weather.py
   ```

## 💡 使用示例

启动客户端后，你可以进行以下查询：

```
Query: 帮我查询纽约的天气预报
Query: 加利福尼亚州有什么天气警报吗？
Query: 北京的经纬度是 39.9042, 116.4074，帮我查询天气
Query: quit  # 退出程序
```

## 🔧 API 接口

### Weather Server 提供的工具

#### `get_forecast(latitude: float, longitude: float)`
- **功能**: 获取指定位置的天气预报
- **参数**: 
  - `latitude`: 纬度
  - `longitude`: 经度
- **返回**: 未来5天的详细天气预报

#### `get_alerts(state: str)`
- **功能**: 获取美国指定州的天气警报
- **参数**: 
  - `state`: 两位字母的州代码 (如 "CA", "NY")
- **返回**: 当前活跃的天气警报列表

## 🛠️ 技术栈

### 服务器端
- **FastMCP**: MCP 服务器框架
- **httpx**: 异步 HTTP 客户端
- **NWS API**: 美国国家气象局天气数据

### 客户端
- **MCP SDK**: Model Context Protocol 客户端
- **OpenAI SDK**: 用于 DeepSeek API 调用
- **python-dotenv**: 环境变量管理

## 📝 开发说明

### 代码特点

- ✅ **完整的中文注释**: 所有代码都有详细的中文注释
- ✅ **类型提示**: 使用 Python 类型提示提高代码可读性
- ✅ **异步编程**: 充分利用异步编程提高性能
- ✅ **错误处理**: 完善的异常处理机制
- ✅ **资源管理**: 正确的异步资源管理

### 扩展开发

要添加新的工具功能：

1. 在 `weather.py` 中使用 `@mcp.tool()` 装饰器定义新函数
2. 实现相应的业务逻辑
3. 客户端会自动识别并可以调用新工具

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 [LICENSE](LICENSE) 许可证。

## 🙋‍♂️ 常见问题

### Q: 如何获取 DeepSeek API Key？
A: 访问 [DeepSeek 官网](https://www.deepseek.com) 注册账号并获取 API Key。

### Q: 支持其他天气数据源吗？
A: 目前仅支持美国国家气象局 API，但可以扩展支持其他数据源。

### Q: 可以连接其他 LLM 吗？
A: 是的，客户端使用 OpenAI SDK，理论上支持所有兼容 OpenAI API 的服务。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发起 Discussion

---

**Happy Coding! 🎉**
