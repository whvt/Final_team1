
FROM python:3.11


WORKDIR /app


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p /app/allure-results

EXPOSE 5050

CMD ["sh", "-c", "pytest -v --alluredir allure-results --clean-alluredir"]

