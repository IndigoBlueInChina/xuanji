# 玄机一撮 (Xuanji)

基于邵康节一撮金的周易解卦系统，使用Streamlit构建的现代化易经解卦应用。

## 功能特点

- 支持输入问题、背景和可能的外应
- 提供64卦完整选择
- 支持动爻选择
- 支持OpenAI API及兼容模式，可连接自定义LLM服务
- 支持导出为Markdown和PDF格式
- 优雅的用户界面

## 安装要求

- Python 3.11 或更高版本
- Poetry 包管理器

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/xuanji.git
cd xuanji
```

2. 使用Poetry安装依赖：
```bash
poetry install --no-root
```

3. 配置环境变量：
将`env.example`文件复制为`.env`并填入您的API配置信息：
```bash
cp env.example .env
```
然后编辑`.env`文件：
```
# LLM 服务API
LLM_SERVICE_API_KEY=your_api_key_here

# 如使用其他LLM服务 (可选)
LLM_SERVICE_BASE_URL=your_api_base_url
LLM_SERVICE_MODEL=your_model_name
```

4. 运行应用：
```bash
poetry run streamlit run app.py
```

## LLM配置选项

应用支持以下配置选项：

1. **OpenAI官方API**：
   - 设置`LLM_SERVICE_API_KEY`：您的OpenAI API密钥
   - 设置`LLM_SERVICE_BASE_URL`：https://api.openai.com/v1
   - 设置`LLM_SERVICE_MODEL`：gpt-4-turbo-preview 或其他OpenAI模型

2. **自定义OpenAI兼容API**：
   - 设置`LLM_SERVICE_API_KEY`：您的API密钥
   - 设置`LLM_SERVICE_BASE_URL`：API基础URL（例如：http://localhost:1234/v1）
   - 设置`LLM_SERVICE_MODEL`：模型名称（例如：qwen-plus 或 llama3-70b）

## 使用说明

1. 在左侧输入区域填写：
   - 所问问题
   - 相关背景（可选）
   - 可能的外应（可选）

2. 在右侧选择：
   - 卦象（64卦中选择）
   - 动爻（可多选）

3. 点击"开始解卦"按钮获取解读结果

4. 可以选择将结果导出为：
   - Markdown格式
   - PDF格式

## 注意事项

- 使用前请确保已正确配置API密钥
- PDF导出功能需要系统安装中文字体（simsun.ttc）
- 建议详细填写问题背景以获得更准确的解读
- 如使用本地LLM，请确保模型对中文理解有良好支持

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目。 