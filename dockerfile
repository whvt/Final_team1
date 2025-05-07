
FROM selenium/standalone-chrome

USER root

WORKDIR /app


COPY requirements.txt .
RUN sudo apt-get install -y python3
RUN sudo apt-get install -y python3-pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p /app/allure-results

EXPOSE 5050

CMD ["pytest", "-v", "--alluredir=allure-results"]
