FROM python:3.9-alpine

WORKDIR /app
ENV REDIS_HOST=
ENV REDIS_PORT=
ENV REDIS_PASSWORD=
ENV GENIUS_API_TOKEN=
ENV DYNAMODB_REGION=
ENV DYNAMODB_TABLE_NAME=
COPY requirements.txt .


RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir /root/.aws
COPY .aws /root/.aws/
CMD ["python3", "app.py"]
