{%- set cc = cookiecutter -%}
{%- set max_ver = cc.python_max_version | int -%}
{% if cc.include_nvidia == "yes" -%}
FROM nvidia/cuda:12.2.2-base-ubuntu22.04 AS base
{%- else -%}
FROM ubuntu:22.04 AS base
{%- endif %}

USER root

# coloring syntax for headers
ENV CYAN='\033[0;36m'
ENV CLEAR='\033[0m'
ENV DEBIAN_FRONTEND="noninteractive"

# setup ubuntu user
ARG UID_="1000"
ARG GID_="1000"
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
    apt update --fix-missing && \
    apt install -y \
        curl \
        software-properties-common && \
    rm -rf /var/lib/apt/lists/*

{%- if cc.include_gcc == "yes" %}

# install gcc
ENV CC=gcc
ENV CXX=g++
RUN echo "\n${CYAN}INSTALL GCC${CLEAR}"; \
    apt update && \
    apt install -y \
        build-essential \
        g++ \
        gcc \
        zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*
{%- endif %}

{%- if cc.include_nvidia == "yes" %}

# install nvidia container toolkit
RUN echo "\n${CYAN}INSTALL NVIDIA CONTAINER TOOLKIT${CLEAR}"; \
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
        | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
        | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
    sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
    apt update && \
    apt install -y \
        libgl1-mesa-glx \
        nvidia-container-toolkit && \
    rm -rf /var/lib/apt/lists/*
{%- endif %}

{%- if cc.include_openexr == "yes" %}

# install OpenEXR
ENV LD_LIBRARY_PATH='/usr/include/python3.{{ max_ver }}m/dist-packages'
RUN echo "\n${CYAN}INSTALL OPENEXR${CLEAR}"; \
    apt update && \
    apt install -y \
        libopenexr-dev \
        openexr && \
    rm -rf /var/lib/apt/lists/*
{%- endif %}

# install python3.{{ max_ver }} and pip
RUN echo "\n${CYAN}SETUP PYTHON3.{{ max_ver }}${CLEAR}"; \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install --fix-missing -y \
        python3.{{ max_ver }}-dev \
        python3.{{ max_ver }}-venv && \
    rm -rf /var/lib/apt/lists/*

# install pip
RUN echo "\n${CYAN}INSTALL PIP${CLEAR}"; \
    curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.{{ max_ver }} get-pip.py && \
    pip3.{{ max_ver }} install --upgrade pip && \
    rm -rf get-pip.py

# install pdm
USER ubuntu
ENV PATH="$PATH:/home/ubuntu/.local/bin"
RUN echo "\n${CYAN}INSTALL PDM${CLEAR}"; \
    curl -sSL \
    https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py \
    | python3.{{ max_ver }} - && \
    pip3.{{ max_ver }} install --upgrade --user pdm && \
    pdm self update --pip-args='--user'

# setup pdm environment
RUN echo "\n${CYAN}SETUP PDM${CLEAR}"; \
    mkdir /home/ubuntu/pdm && \
    cd /home/ubuntu/pdm && \
    pdm init --python 3.{{ max_ver }} --non-interactive && \
    rm -rf src tests README.md __pycache__ .gitignore && \
    pdm venv create -n prod-3.{{ max_ver }};

# install {{ cc.repo }}
USER ubuntu
COPY --chown=ubuntu:ubuntu config/prod.toml /home/ubuntu/pdm/pyproject.toml
ARG VERSION
{%- if cc.include_secret_env == 'yes' %}
ARG URL="YOUR PRIVATE PYPI URL"
RUN --mount=type=secret,id=secret-env,mode=0444 \
    . /run/secrets/secret-env && \
    echo "\n${CYAN}INSTALL {{ cc.repo | upper }}${CLEAR}"; \
    cd /home/ubuntu/pdm && \
    pdm add -v {{ cc.repo }}==$VERSION;
{%- else %}
RUN echo "\n${CYAN}INSTALL {{ cc.repo | upper }}${CLEAR}"; \
    cd /home/ubuntu/pdm && \
    pdm add -v "{{ cc.repo }}==$VERSION";
{%- endif %}

ENV PATH="/home/ubuntu/pdm/.venv/bin:$PATH"
