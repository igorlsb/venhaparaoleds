FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#flask
EXPOSE 5010

#comando para iniciar a aplicação
CMD ["python", "application.py"]
