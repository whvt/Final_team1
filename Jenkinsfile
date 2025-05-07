pipeline {
    agent any

    environment {
        GIT_URL = 'https://github.com/whvt/Final_team1'
        GIT_CREDENTIALS = 'GITHUB_CREDENTIALS'
        DOCKER_IMAGE = 'teamone'
        ALLURE_RESULTS_DIR = 'reports'
        ALLURE_REPORT_DIR = 'reports_html'
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
                sh 'docker run --rm -v $(pwd)/$ALLURE_RESULTS_DIR:/allure-results $DOCKER_IMAGE pytest -v --alluredir=/allure-results'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate $ALLURE_RESULTS_DIR -o $ALLURE_REPORT_DIR'
            }
        }

        stage('Publish Report') {
            steps {
                allure([
                    results: [[path: ALLURE_RESULTS_DIR]]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "$ALLURE_REPORT_DIR/**/*", allowEmptyArchive: true
        }
    }
}
