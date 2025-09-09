FROM mcr.microsoft.com/devcontainers/python:3.13 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

ARG EXTRA_NODE_VERSION=22
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${EXTRA_NODE_VERSION} && npm install -g @google/gemini-cli" 2>&1 
