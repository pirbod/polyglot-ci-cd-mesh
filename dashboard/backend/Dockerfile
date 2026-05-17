FROM python:3.12-slim
WORKDIR /app
COPY dashboard/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dashboard/backend ./dashboard/backend
COPY security-gates ./security-gates
COPY scripts/generate_demo_data.py ./scripts/generate_demo_data.py
WORKDIR /app/dashboard/backend
RUN python /app/scripts/generate_demo_data.py
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
