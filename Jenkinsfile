pipeline {
    agent any

    environment {
        GIT_URL = 'https://github.com/whvt/Final_team1'
        GIT_CREDENTIALS = 'GITHUB_TOKEN'
        DOCKER_IMAGE = 'teamone'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: "$GIT_CREDENTIALS", url: "$GIT_URL"
            }
        }

        stage('Build & Test') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
                sh 'docker run --rm $DOCKER_IMAGE pytest --alluredir=reports'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate reports -o reports_html'
            }
        }

        stage('Publish Report') {
            steps {
                allure([
                    results: [[path: 'reports_html']]
                ])
            }
        }
    }
}
