FROM python:3.8-slim

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++ \
        git && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get install libgomp1 -y

COPY requirements.txt /code/app/
ENV PYTHONPATH=$PYTHONPATH:/code/app
ENV MLFLOW_S3_ENDPOINT_URL=
ENV AWS_ACCESS_KEY_ID=12
ENV AWS_SECRET_ACCESS_KEY=12
ENV AWS_DEFAULT_REGION="asia"

RUN pip install --no-cache-dir -r /code/app/requirements.txt

EXPOSE 8000

COPY ./app /code/app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]