pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/ТВОЙ_ЛОГИН/ci-docker-sample.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t myapp:latest .'
                }
            }
        }
    }
}
