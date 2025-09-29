ARG VARIANT=ubuntu-22.04
FROM mcr.microsoft.com/devcontainers/base:${VARIANT}

LABEL dev.containers.features="common"

WORKDIR /home/vscode

COPY post_create.sh chezmoi.toml /usr/src/
RUN chmod +x /usr/src/post_create.sh

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    pip libzip-dev unzip tmux direnv ranger curl neovim wget autoconf python3-docutils \
    && apt-get clean

# Install argbash with proper library files
RUN cd /tmp && \
    wget https://github.com/matejak/argbash/archive/refs/tags/2.11.0.tar.gz -O argbash.tar.gz && \
    tar -xzf argbash.tar.gz && \
    cd argbash-2.11.0/resources && \
    make install PREFIX=/usr/local && \
    cd / && rm -rf /tmp/argbash*

COPY requirements.txt /usr/src/
RUN pip install -r /usr/src/requirements.txt

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash - && \
    apt-get install -y nodejs

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm install

# Add node_modules/.bin to PATH
ENV PATH=/home/vscode/node_modules/.bin:$PATH
