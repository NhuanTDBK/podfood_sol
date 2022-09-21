# Introduction
PodFood Demo Prediction is a backend service which predict next quantity by store and product

# Structures

- build:  contains Dockerfile to build service
- src:
  - python:
    - webserver: Online Serving API
    - notebook: Modelling and Data Exploration
- docker-compose.yaml

# How-to-use

## Install environment

Create conda environment

```bash
conda create -n podfood python=3.8
conda activate podfood
```

## Start backend services

```bash
docker compose up
```

## Data Exploration and Modelling

Execute all cells in the notebook. When the notebook finished, model will be stored in MLFlow so API can be ready to serve

```bash
cd src/python/notebook && juypyter lab
```

## Do some CURLS

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/ml/forecast' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "requests": [
    {
      "store_id": 10,
      "product_id": 2071
    }
  ],
  "model_version": "latest",
  "predicted_date": "string"
}'
```

## Monitoring

Grafana and Prometheus are already integrated with Serving API. Follow the instructions to create dashboard

- Go to `localhost:3000`
- Login with `admin|pass@123`
- Create datasource Prometheus with link `http://prometheus:9090`
- Create new dashboard by `Import`. Get the template in `build/grafana/dashboards/fastapi-dashboard.json`

![grafana](grafana.png)