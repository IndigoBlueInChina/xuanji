# 第一阶段：构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖（Poetry 和 pycairo 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    pkg-config \
    libcairo2-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Poetry 最新版本
RUN pip install --no-cache-dir poetry

# 配置 Poetry：不使用虚拟环境，直接安装到系统 Python
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# 复制依赖文件
COPY pyproject.toml poetry.lock ./

# 安装依赖（不安装项目本身，因为 package-mode = false）
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# 第二阶段：运行阶段
FROM python:3.11-slim as runtime

# 设置工作目录
WORKDIR /app

# 安装运行时系统依赖（包括 cairo 运行时库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制已安装的 Python 包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制应用代码
COPY app.py ./
COPY hexagram_*.py ./
COPY services/ ./services/
COPY utils/ ./utils/
COPY styles/ ./styles/
COPY xuanji/ ./xuanji/

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import streamlit; print('OK')" || exit 1

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

