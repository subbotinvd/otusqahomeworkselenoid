FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SHOP_URL=http://host.docker.internal:8080 \
    HEADLESS=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium chromium-driver firefox-esr ca-certificates curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL \
        https://github.com/mozilla/geckodriver/releases/download/v0.37.1/geckodriver-v0.37.1-linux64.tar.gz \
        -o /tmp/geckodriver.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
    && rm /tmp/geckodriver.tar.gz

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["pytest"]
CMD ["tests/"]
