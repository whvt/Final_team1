FROM selenium/standalone-chrome:latest

USER root

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/allure-results

EXPOSE 5050

CMD ["pytest", "-v", "--alluredir=allure-results"]