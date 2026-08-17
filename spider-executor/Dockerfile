FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system spider \
    && useradd --system --gid spider --home /app spider
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
COPY README.md AGENTS.md ./
RUN uv sync --frozen --no-dev && mkdir -p /srv/spider/artifacts /srv/spider/repositories && chown -R spider:spider /app /srv/spider
USER spider
EXPOSE 8000
CMD ["uvicorn", "spider_executor.main:app", "--host", "0.0.0.0", "--port", "8000"]
