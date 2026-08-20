FROM python:3.13-slim

ARG SPIDER_EXECUTOR_UID=1000
ARG SPIDER_EXECUTOR_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PATH="/app/.venv/bin:$PATH"     PYTHONPATH=/app/src

RUN case "$SPIDER_EXECUTOR_UID:$SPIDER_EXECUTOR_GID" in \
        *[!0-9:]*|:*|*:|*:*:*) echo "invalid Executor UID/GID" >&2; exit 1 ;; \
    esac \
    && [ "$SPIDER_EXECUTOR_UID" -ge 1 ] \
    && [ "$SPIDER_EXECUTOR_UID" -le 65534 ] \
    && [ "$SPIDER_EXECUTOR_GID" -ge 1 ] \
    && [ "$SPIDER_EXECUTOR_GID" -le 65534 ] \
    && apt-get update && apt-get install -y --no-install-recommends git openssh-client \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid "$SPIDER_EXECUTOR_GID" spider \
    && useradd --uid "$SPIDER_EXECUTOR_UID" --gid "$SPIDER_EXECUTOR_GID" \
        --home-dir /app --no-create-home --shell /usr/sbin/nologin spider
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
COPY README.md AGENTS.md ./
RUN mkdir -p /srv/spider/artifacts /srv/spider/repositories && chown -R spider:spider /app /srv/spider
USER spider
EXPOSE 8000
CMD ["uvicorn", "spider_executor.main:app", "--host", "0.0.0.0", "--port", "8000"]
