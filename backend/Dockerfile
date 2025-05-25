FROM python:3.13-alpine@sha256:452682e4648deafe431ad2f2391d726d7c52f0ff291be8bd4074b10379bb89ff

RUN apk update && \
    apk add --no-cache bash build-base libpq-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app/ app/
COPY tests/ tests/

ENTRYPOINT []
CMD ["python", "main.py"]