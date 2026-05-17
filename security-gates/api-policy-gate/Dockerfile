FROM python:3.12-slim
WORKDIR /app
COPY security-gates/api-policy-gate/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY security-gates/api-policy-gate .
EXPOSE 8090
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
