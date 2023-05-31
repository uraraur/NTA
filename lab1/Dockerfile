FROM jupyter/base-notebook

USER root

RUN apt-get update \
    && echo "Updated apt-get" \
    && apt-get install -y openjdk-8-jre \
    && echo "Installed openjdk 8"
    
RUN conda install -y -c jetbrains kotlin-jupyter-kernel && echo "Kotlin Jupyter kernel installed via conda"

USER $NB_UID

ENV JUPYTER_ENABLE_LAB=yes