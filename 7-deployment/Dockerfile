

FROM docker.io/library/python:3.11-slim

WORKDIR /app

COPY *.py .

RUN pip install flask requests && mkdir /app/static

#COPY sample.jpg /app/static

EXPOSE 5000

CMD ["python", "app.py"]

