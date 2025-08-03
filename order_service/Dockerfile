FROM python:3.10-slim
WORKDIR /app
COPY order_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./order_service .
COPY common/ common/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]