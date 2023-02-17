{%- set max_ver = cookiecutter.python_max_version | int -%}
{% if cookiecutter.include_tensorflow == "yes" -%}
FROM tensorflow/tensorflow:nightly-gpu AS base
{%- else -%}
FROM ubuntu:22.04 AS base
{%- endif %}

USER root

# coloring syntax for headers
ENV CYAN='\033[0;36m'
ENV CLEAR='\033[0m'
ENV DEBIAN_FRONTEND='noninteractive'

# setup ubuntu user
ARG UID_='1000'
ARG GID_='1000'
RUN echo "\n${CYAN}SETUP UBUNTU USER${CLEAR}"; \
    addgroup --gid $GID_ ubuntu && \
    adduser \
        --disabled-password \
        --gecos '' \
        --uid $UID_ \
        --gid $GID_ ubuntu
WORKDIR /home/ubuntu

# update ubuntu and install basic dependencies
RUN echo "\n${CYAN}INSTALL GENERIC DEPENDENCIES${CLEAR}"; \
    apt update && \
    apt install -y \
        software-properties-common \
        wget && \
    rm -rf /var/lib/apt/lists/*

# install python3.{{ max_ver }} and pip
RUN echo "\n${CYAN}SETUP PYTHON3.{{ max_ver }}${CLEAR}"; \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install --fix-missing -y python3.{{ max_ver }} && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.{{ max_ver }} get-pip.py && \
    rm -rf /home/ubuntu/get-pip.py

# install {{cookiecutter.repo}}
USER ubuntu
ENV REPO='{{cookiecutter.repo}}'
ENV PYTHONPATH "${PYTHONPATH}:/home/ubuntu/$REPO/python"
RUN echo "\n${CYAN}INSTALL {{cookiecutter.repo}}{CLEAR}"; \
    pip3.{{ max_ver }} install --user --upgrade {{cookiecutter.repo}}
