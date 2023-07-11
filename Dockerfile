FROM python:3.11.4-alpine3.17
WORKDIR /app/src
ADD src / /app/src/
COPY assets/config.yaml /etc/crawler_config.yaml
RUN pip install -r requirements.txt
CMD ["python", "main.py"]