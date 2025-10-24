node {
    stage('Build Docker Image') {
        sh 'docker build -t myapp:latest .'
    }

    stage('Run and Test') {
        sh '''
            docker run --rm \
                -e CELL_1=A1 \
                -e CELL_2=H8 \
                -e FIGURE=ферзь \
                myapp:latest
        '''
    }

    stage('Push to Docker Hub') {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh '''
                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                docker tag myapp:latest $DOCKER_USER/myapp:latest
                docker push $DOCKER_USER/myapp:latest
            '''
        }
    }
}
