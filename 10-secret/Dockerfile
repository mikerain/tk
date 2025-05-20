

FROM docker.io/library/python:3.11-slim

WORKDIR /app

RUN pip install -i  https://pypi.tuna.tsinghua.edu.cn/simple flask requests configparser pymysql mysql-connector-python  && mkdir /app/static /app/templates /app/config

COPY *.py /app
#COPY sample.jpg /app/static
COPY index.html /app/templates
COPY config.ini /app/config

EXPOSE 5000

CMD ["python", "app.py"]

