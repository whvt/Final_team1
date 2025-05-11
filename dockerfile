
FROM selenium/standalone-chrome
USER root

WORKDIR /app


COPY requirements.txt .


RUN sudo apt-get update
RUN sudo apt-get install -y python3
RUN sudo apt-get install -y python3-pip
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/allure-results

EXPOSE 5050

CMD ["pytest", "-s", "-v", "--alluredir=allure-results"]