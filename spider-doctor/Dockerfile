FROM astral/uv:0.12.1@sha256:cf4eedcaa81655197f625739489effcbe71b61ceb1506f332c3facae5deceded AS uv
FROM docker:29.7.2-cli@sha256:000bb62ff495f986c9f5578eb67cc2cb98b91138eda81d7762d5371eb8a497fe AS docker-cli
FROM python:3.13-slim-bookworm@sha256:00faa2debb87529f9f0764e9491d8ba400a3678976616c3bd7cb193745ac20d1

ARG SPIDER_DOCTOR_UID
ARG SPIDER_DOCTOR_GID

COPY --from=uv /uv /uvx /usr/local/bin/
COPY --from=docker-cli /usr/local/bin/docker /usr/local/bin/docker

RUN case "$SPIDER_DOCTOR_UID:$SPIDER_DOCTOR_GID" in \
        *[!0-9:]*|:*|*:|*:*:*) echo "invalid Doctor UID/GID" >&2; exit 1 ;; \
    esac \
    && [ "$SPIDER_DOCTOR_UID" -ge 1 ] \
    && [ "$SPIDER_DOCTOR_UID" -le 65534 ] \
    && [ "$SPIDER_DOCTOR_GID" -ge 1 ] \
    && [ "$SPIDER_DOCTOR_GID" -le 65534 ] \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git openssh-client \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid "$SPIDER_DOCTOR_GID" doctor \
    && useradd --uid "$SPIDER_DOCTOR_UID" --gid "$SPIDER_DOCTOR_GID" \
        --home-dir /home/doctor --create-home --shell /usr/sbin/nologin doctor \
    && chmod 0755 /home/doctor

WORKDIR /opt/spider-doctor
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

ENV PATH=/opt/spider-doctor/.venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["spider-doctor-worker"]
