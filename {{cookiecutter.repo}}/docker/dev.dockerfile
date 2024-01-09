{%- set cc = cookiecutter -%}
{%- set min_ver = cc.python_min_version | int %}
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
        --gid $GID_ ubuntu && \
    usermod -aG root ubuntu

# setup sudo
RUN echo "\n${CYAN}SETUP SUDO${CLEAR}"; \
    apt update && \
    apt install -y sudo && \
    usermod -aG sudo ubuntu && \
    echo '%ubuntu    ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu

# update ubuntu and install basic dependencies
RUN echo "\n${CYAN}INSTALL GENERIC DEPENDENCIES${CLEAR}"; \
    apt update && \
    apt install -y \
        apt-transport-https \
        bat \
        btop \
        ca-certificates \
        curl \
        exa \
        git \
        gnupg \
        graphviz \
        jq \
        parallel \
        ripgrep \
{% if cc.include_rsync == "yes" -%}
        rsync \
{%- endif %}
        software-properties-common \
        unzip \
        vim \
        wget && \
    rm -rf /var/lib/apt/lists/*

# install yq
RUN echo "\n${CYAN}INSTALL YQ${CLEAR}"; \
    curl -fsSL \
        https://github.com/mikefarah/yq/releases/download/v4.9.1/yq_linux_amd64 \
        -o /usr/local/bin/yq && \
    chmod +x /usr/local/bin/yq

# install all python versions
RUN echo "\n${CYAN}INSTALL PYTHON${CLEAR}"; \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y \
        python3-pydot \
    {%- for version in range(min_ver, max_ver + 1) | reverse %}
        python3.{{ version }}-dev \
        python3.{{ version }}-venv \
        python3.{{ version }}-distutils \
    {%- endfor %}
    && rm -rf /var/lib/apt/lists/*

# install pip
RUN echo "\n${CYAN}INSTALL PIP${CLEAR}"; \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.{{ max_ver }} get-pip.py && \
    pip3.{{ max_ver }} install --upgrade pip && \
    rm -rf get-pip.py

# install nodejs (needed by jupyter lab)
RUN echo "\n${CYAN}INSTALL NODEJS${CLEAR}"; \
    sudo mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    export NODE_VERSION=18 && \
    echo "deb \
        [signed-by=/etc/apt/keyrings/nodesource.gpg] \
        https://deb.nodesource.com/node_$NODE_VERSION.x \
        nodistro main" \
        | sudo tee /etc/apt/sources.list.d/nodesource.list && \
    sudo apt update && \
    sudo apt install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# install and setup zsh
RUN echo "\n${CYAN}SETUP ZSH${CLEAR}"; \
    apt update && \
    apt install -y zsh && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh \
        -o install-oh-my-zsh.sh && \
    echo y | sh install-oh-my-zsh.sh && \
    mkdir -p /root/.oh-my-zsh/custom/plugins && \
    cd /root/.oh-my-zsh/custom/plugins && \
    git clone https://github.com/zdharma-continuum/fast-syntax-highlighting && \
    git clone https://github.com/zsh-users/zsh-autosuggestions && \
    npm i -g zsh-history-enquirer --unsafe-perm && \
    cd /home/ubuntu && \
    cp -r /root/.oh-my-zsh /home/ubuntu/ && \
    chown -R ubuntu:ubuntu .oh-my-zsh && \
    rm -rf install-oh-my-zsh.sh && \
    echo 'UTC' > /etc/timezone

# install s6-overlay
RUN echo "\n${CYAN}INSTALL S6${CLEAR}"; \
    export S6_ARCH="x86_64" && \
    export S6_VERSION="v3.1.5.0" && \
    export S6_URL="https://github.com/just-containers/s6-overlay/releases/download" && \
    curl -fsSL "${S6_URL}/${S6_VERSION}/s6-overlay-noarch.tar.xz" \
        -o /tmp/s6-overlay-noarch.tar.xz && \
    curl -fsSL "${S6_URL}/${S6_VERSION}/s6-overlay-noarch.tar.xz.sha256" \
        -o /tmp/s6-overlay-noarch.tar.xz.sha256 && \
    curl -fsSL "${S6_URL}/${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
        -o /tmp/s6-overlay-${S6_ARCH}.tar.xz && \
    curl -fsSL "${S6_URL}/${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz.sha256" \
        -o /tmp/s6-overlay-${S6_ARCH}.tar.xz.sha256 && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-${S6_ARCH}.tar.xz && \
    rm /tmp/s6-overlay-noarch.tar.xz \
       /tmp/s6-overlay-noarch.tar.xz.sha256 \
       /tmp/s6-overlay-${S6_ARCH}.tar.xz \
       /tmp/s6-overlay-${S6_ARCH}.tar.xz.sha256

{%- if cc.include_vscode_server == "yes" %}

# install vscode server
RUN echo "\n${CYAN}INSTALL VSCODE SERVER${CLEAR}"; \
    export CODE_ARCH="amd64" && \
    export CODE_VERSION="4.19.1" && \
    export CODE_URL="https://github.com/coder/code-server/releases/download/v$CODE_VERSION/code-server_${CODE_VERSION}_$CODE_ARCH.deb" && \
    curl -fsSL $CODE_URL -o /tmp/code-server.deb && \
    dpkg -i /tmp/code-server.deb && \
    rm -f /tmp/code-server.deb
{%- endif %}

USER ubuntu
ENV PATH="/home/ubuntu/.local/bin:$PATH"
COPY ./config/henanigans.zsh-theme .oh-my-zsh/custom/themes/henanigans.zsh-theme

ENV LANG "C.UTF-8"
ENV LANGUAGE "C.UTF-8"
ENV LC_ALL "C.UTF-8"
# ------------------------------------------------------------------------------

FROM base AS dev
USER root
{%- if cc.repo_type == 'dash' %}

# install chromedriver
ENV PATH=$PATH:/lib/chromedriver
RUN echo "\n${CYAN}INSTALL CHROMEDRIVER${CLEAR}"; \
    apt update && \
    apt install -y chromium-chromedriver && \
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

{% if cc.include_openexr == "yes" -%}
# install OpenEXR
ENV CC=gcc
ENV CXX=g++
ENV LD_LIBRARY_PATH='/usr/include/python3.{{ max_ver }}m/dist-packages'
RUN echo "\n${CYAN}INSTALL OPENEXR${CLEAR}"; \
    apt update && \
    apt install -y \
        build-essential \
        g++ \
        gcc \
        libopenexr-dev \
        openexr \
        zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*
{%- endif %}

USER ubuntu
WORKDIR /home/ubuntu

# install dev dependencies
RUN echo "\n${CYAN}INSTALL DEV DEPENDENCIES${CLEAR}"; \
    curl -sSL \
        https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py \
        | python3.{{ max_ver }} - && \
    pip3.{{ max_ver }} install --upgrade --user \
        pdm \
        'pdm-bump<0.7.0' \
        'rolling-pin>=0.9.2' && \
    mkdir -p /home/ubuntu/.oh-my-zsh/custom/completions && \
    pdm self update --pip-args='--user' && \
    pdm completion zsh > /home/ubuntu/.oh-my-zsh/custom/completions/_pdm

# setup pdm
COPY --chown=ubuntu:ubuntu config/build.yaml /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/dev.lock /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/pdm.toml /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/prod.lock /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/pyproject.toml /home/ubuntu/config/
{%- if cc.include_prod_cli == 'yes' %}
COPY --chown=ubuntu:ubuntu scripts/prod-cli /home/ubuntu/scripts/
{%- endif %}
COPY --chown=ubuntu:ubuntu scripts/x_tools.sh /home/ubuntu/scripts/
RUN echo "\n${CYAN}SETUP DIRECTORIES${CLEAR}"; \
    mkdir pdm

# create dev env
WORKDIR /home/ubuntu/pdm
RUN echo "\n${CYAN}INSTALL DEV ENVIRONMENT${CLEAR}"; \
    . /home/ubuntu/scripts/x_tools.sh && \
    export CONFIG_DIR=/home/ubuntu/config && \
    export SCRIPT_DIR=/home/ubuntu/scripts && \
    x_env_init dev 3.{{ max_ver }} && \
    cd /home/ubuntu && \
    ln -s `_x_env_get_path dev 3.{{ max_ver }}` .dev-env && \
    ln -s `_x_env_get_path dev 3.{{ max_ver }}`/lib/python3.{{ max_ver }}/site-packages .dev-packages

# create prod envs
RUN echo "\n${CYAN}INSTALL PROD ENVIRONMENTS${CLEAR}"; \
    . /home/ubuntu/scripts/x_tools.sh && \
    export CONFIG_DIR=/home/ubuntu/config && \
    export SCRIPT_DIR=/home/ubuntu/scripts && \
{%- for version in range(min_ver + 1, max_ver + 1) | reverse %}
    x_env_init prod 3.{{ version }} && \
{%- endfor %}
    x_env_init prod 3.{{ min_ver }}

{%- if cc.include_prod_cli == 'yes' %}

# install prod cli
RUN echo "\n${CYAN}INSTALL PROD CLI${CLEAR}"; \
    cp /home/ubuntu/scripts/prod-cli /home/ubuntu/.local/bin/{{ cc.repo }} && \
    chmod 755 /home/ubuntu/.local/bin/{{ cc.repo }}
{%- endif %}

# build jupyter lab
RUN echo "\n${CYAN}BUILD JUPYTER LAB${CLEAR}"; \
    . /home/ubuntu/scripts/x_tools.sh && \
    export CONFIG_DIR=/home/ubuntu/config && \
    export SCRIPT_DIR=/home/ubuntu/scripts && \
    x_env_activate_dev && \
    jupyter lab build

USER root

# add s6 service and init scripts
COPY --chown=ubuntu:ubuntu --chmod=755 scripts/s_tools.sh /home/ubuntu/scripts/
RUN echo "\n${CYAN}SETUP S6 SERVICES${CLEAR}"; \
    . /home/ubuntu/scripts/s_tools.sh && \
    s_setup_services

USER ubuntu
WORKDIR /home/ubuntu

# cleanup dirs
RUN echo "\n${CYAN}REMOVE DIRECTORIES${CLEAR}"; \
    rm -rf /home/ubuntu/config /home/ubuntu/scripts

ENV REPO='{{cc.repo}}'
ENV PYTHONPATH ":/home/ubuntu/$REPO/python:/home/ubuntu/.local/lib"
ENV PYTHONPYCACHEPREFIX "/home/ubuntu/.python_cache"
ENV HOME /home/ubuntu
ENV JUPYTER_RUNTIME_DIR /tmp/jupyter_runtime

EXPOSE 8888/tcp
ENTRYPOINT ["/init"]
