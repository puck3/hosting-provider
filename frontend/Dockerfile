FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN apk update && \
    apk add --no-cache bash build-base libpq-dev

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN uv venv && \ 
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"


COPY main.py .
COPY src/ src/

EXPOSE 8501

ENTRYPOINT []
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]