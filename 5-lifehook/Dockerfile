

FROM docker.io/library/python:3.11-slim

WORKDIR /app


RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  flask requests && mkdir /app/static

COPY *.py .
COPY sample.jpg /app/static

EXPOSE 5000

CMD ["python", "app.py"]

