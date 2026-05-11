# 基础镜像：轻量级Python 3.13
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 替换为阿里云 Debian 源（适用于 Debian trixie 或 bookworm，根据你的基础镜像版本）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

# 然后安装 curl
RUN apt-get update && apt-get install -y curl

# 先装uv（依赖管理器）
RUN pip install uv

# 复制依赖定义文件
COPY pyproject.toml uv.lock ./

# 安装项目依赖
RUN uv sync

# 复制后端代码
COPY app.py ./

# 暴露Flask端口
EXPOSE 5000

# 容器启动时运行Flask
CMD ["uv", "run", "app.py"]
