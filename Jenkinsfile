pipeline {
    agent any

    environment {
        GIT_URL = 'https://github.com/whvt/Final_team1'
        GIT_CREDENTIALS = 'GITHUB_CREDENTIALS'
        ALLURE_RESULTS_DIR = 'reports'
        ALLURE_REPORT_DIR = 'reports_html'
        ALLURE_CMD = '/var/lib/jenkins/allure/allure-2.34.0/bin/allure'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: "$GIT_CREDENTIALS", url: "$GIT_URL"
            }
        }

        stage('Preparation') {
            steps {
                script {
                    echo 'Installing Allure'
                    sh '''
                        mkdir -p /var/lib/jenkins/allure
                        wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.34.0/allure-commandline-2.34.0.zip -O /var/lib/jenkins/allure/allure.zip
                        unzip -o /var/lib/jenkins/allure/allure.zip -d /var/lib/jenkins/allure
                        chown -R jenkins:jenkins /var/lib/jenkins/allure
                        chmod -R 775 /var/lib/jenkins/allure
                    '''
                }
            }
        }

        stage('Build & Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh 'docker build -t teamone .'
                    sh 'docker run --rm --network=host -v $(pwd)/$ALLURE_RESULTS_DIR:/allure-results teamone pytest -v --alluredir=/allure-results'
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                    sh '/var/lib/jenkins/allure/allure-2.34.0/bin/allure generate reports -o reports_html --clean'
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
            archiveArtifacts artifacts: "${env.ALLURE_REPORT_DIR}/**/*", allowEmptyArchive: true
        }
    }
}
