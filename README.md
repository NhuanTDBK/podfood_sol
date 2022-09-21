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

Execute all cells in the notebook

```bash
cd src/python/notebook && juypyter lab
```
