
# 玄机一撮 (Xuanji)

基于邵康节一撮金的周易解卦系统，使用Streamlit构建的现代化易经解卦应用。

![玄机一撮](https://img.shields.io/badge/玄机一撮-v0.1.0-blue)

## 功能概述

玄机一撮是一款基于邵康节一撮金理论的周易解卦系统，通过现代人工智能技术，为用户提供专业、详细的卦象解读。

## 主要功能

- **卦象解读**：提供64卦完整选择，支持动爻选择
- **多维分析**：自动计算并展示本卦、变卦、交互卦、综卦的关系
- **一撮金原文**：根据卦象和动爻自动匹配邵康节一撮金原文
- **流式输出**：实时生成解卦结果，提供流畅的用户体验
- **导出功能**：支持将解卦结果导出为Markdown和HTML格式（可打印为PDF）
- **卦图可视化**：直观展示卦象图形，包括动爻标记

## 使用指南

### 基本操作流程

1. **输入信息**：
   - 在左侧输入区填写"所问何事"（必填）
   - 可选填写"是何因缘"（背景信息）
   - 可选填写"外应"（相关征兆）

2. **选择卦象**：
   - 从64卦中选择一个卦象
   - 根据需要选择动爻（可多选）

3. **获取解读**：
   - 点击"开始解卦"按钮
   - 系统会实时生成解卦结果
   - 解读内容包括卦象分析、时间指示和行动建议

4. **导出结果**：
   - 可将解卦结果导出为Markdown格式
   - 可导出为HTML格式（包含卦图，可打印为PDF）

### 解卦结果内容

解卦结果通常包含以下内容：

- **卦象解读**：结合系辞、卦辞、爻辞、彖辞、象辞和一撮金原文
- **多卦关系**：分析本卦、变卦、交互卦和综卦之间的关系
- **时间指示**：可能的时间范围和影响程度
- **行动建议**：从趋利避害角度给出的具体建议

## 安装与配置

### 系统要求

- Python 3.11 或更高版本
- Poetry 包管理器
- 支持中文显示的操作系统

### 安装步骤

1. **克隆仓库**：
   ```bash
   git clone https://github.com/yourusername/xuanji.git
   cd xuanji
   ```

2. **安装依赖**：
   ```bash
   poetry install --no-root
   ```

3. **配置环境变量**：
   将`env.example`文件复制为`.env`：
   ```bash
   copy env.example .env
   ```
   
   编辑`.env`文件，填入API配置信息：
   ```
   # LLM 服务API密钥设置
   LLM_SERVICE_API_KEY=your_api_key_here
   
   # LLM 服务API地址（兼容OpenAI API格式）
   LLM_SERVICE_BASE_URL=https://api.openai.com/v1
   
   # 使用的模型名称
   LLM_SERVICE_MODEL=qwen-plus
   ```

4. **启动应用**：
   ```bash
   poetry run streamlit run app.py
   ```

### LLM服务配置选项

应用支持多种LLM服务配置：

1. **OpenAI官方API**：
   - `LLM_SERVICE_API_KEY`：您的OpenAI API密钥
   - `LLM_SERVICE_BASE_URL`：https://api.openai.com/v1
   - `LLM_SERVICE_MODEL`：gpt-4-turbo-preview 或其他OpenAI模型

2. **自定义OpenAI兼容API**：
   - `LLM_SERVICE_API_KEY`：您的API密钥
   - `LLM_SERVICE_BASE_URL`：自定义API地址（如：http://localhost:1234/v1）
   - `LLM_SERVICE_MODEL`：模型名称（如：qwen-plus 或 llama3-70b）

## 技术实现

- **前端界面**：使用Streamlit构建直观的用户界面
- **LLM集成**：支持OpenAI API及兼容接口，可连接自定义LLM服务
- **卦象计算**：内置完整的64卦编码系统，支持变卦、交互卦、综卦计算
- **一撮金数据库**：包含邵康节一撮金原文，根据卦象和动爻自动匹配

## 注意事项

- 使用前请确保已正确配置API密钥
- HTML导出功能包含卦图显示，可通过浏览器打印为PDF
- 建议详细填写问题背景以获得更准确的解读
- 如使用本地LLM，请确保模型对中文理解有良好支持

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目。

        