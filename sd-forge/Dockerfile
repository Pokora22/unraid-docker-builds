FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV NVIDIA_VISIBLE_DEVICES=all
ENV PYTHON=/home/forge/sd-webui/venv/bin/python
ENV COMMANDLINE_ARGS=

# ── System deps ───────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── uv ────────────────────────────────────────────────────────────────────────
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# ── Forge user (uid 99 / gid 100 = Unraid nobody/users) ──────────────────────
RUN useradd -u 99 -g 100 -d /home/forge forge

WORKDIR /home/forge

# ── Clone Haoming02 neo branch ────────────────────────────────────────────────
RUN git clone --branch neo --depth 1 \
    https://github.com/Haoming02/sd-webui-forge-classic \
    sd-webui

WORKDIR /home/forge/sd-webui

# ── Set up venv ───────────────────────────────────────────────────────────────
RUN uv venv venv --python python3.13 --seed

RUN chown -R forge:users /home/forge

USER forge

EXPOSE 7860/tcp

CMD ["sh", "-c", "/home/forge/sd-webui/venv/bin/python launch.py --listen $COMMANDLINE_ARGS"]