FROM docker:cli AS docker-cli

FROM python:3.12-slim
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker
WORKDIR /app
RUN pip install --no-cache-dir discord.py
COPY bot.py .
CMD ["python", "bot.py"]
