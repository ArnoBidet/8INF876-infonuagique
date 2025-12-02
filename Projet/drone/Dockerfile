FROM python:3.10-slim

WORKDIR /projet

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "drone_subscriber.py"]