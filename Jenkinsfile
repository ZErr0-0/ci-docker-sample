pipeline {
    agent any

    stages {
        stage('Cleanup Docker') {
            steps {
                sh '''
                    docker builder prune -af || true
                    docker image rm myapp:latest || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t myapp:latest .'
            }
        }

        stage('Run and Test') {
            steps {
                sh 'docker run --rm myapp:latest'
            }
        }
    }
}
