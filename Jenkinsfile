pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = "your_dockerhub_username/myapp"  // замени на свой репозиторий
    }

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

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag myapp:latest $DOCKERHUB_REPO:latest
                        docker push $DOCKERHUB_REPO:latest
                        docker logout
                    '''
                }
            }
        }
    }
}
