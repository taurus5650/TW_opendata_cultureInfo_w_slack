FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN chmod +x entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt
CMD ["./entrypoint.sh"]