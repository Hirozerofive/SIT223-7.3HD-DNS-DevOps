FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dns.py .
COPY client.py .

EXPOSE 5000/udp

CMD ["python", "dns.py"]