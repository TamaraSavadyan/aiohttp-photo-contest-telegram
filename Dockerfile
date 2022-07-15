#syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.9-slim


FROM python:${PYTHON_VERSION} as builder
ENV PYTHONUNBUFFERED=1
ARG PIP_EXTRA_INDEX_URL

RUN apt-get update \
        && apt-get install -y gcc git \
        && pip install -U pip setuptools wheel

WORKDIR /wheels
COPY requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel -r /requirements.txt


FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
RUN pip install -U pip setuptools wheel \
        && pip install /wheels/* \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/*

WORKDIR /code
COPY . .

ENV CONFIG=/app/config.yaml
ENTRYPOINT ["python", "manage.py"]
CMD ["api"]
