FROM python:3.11-slim
WORKDIR /app
COPY reference_impl/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn","reference_impl.app:app","--host","0.0.0.0","--port","8000"]
