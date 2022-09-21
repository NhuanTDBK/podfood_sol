FROM jupyter/pyspark-notebook
WORKDIR /work

RUN pip install lightgbm
RUN pip install --user jupyterlab pandas numpy lightgbm jupyter pyspark

EXPOSE 8888

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]