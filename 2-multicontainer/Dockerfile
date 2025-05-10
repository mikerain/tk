# 使用官方 Python 镜像
FROM docker.io/library/python:3.11-slim

# 设置工作目录
WORKDIR /app

# 拷贝代码到容器
COPY app.py .

# 安装依赖
RUN pip install flask

RUN chmod 777 /var/log
# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]

