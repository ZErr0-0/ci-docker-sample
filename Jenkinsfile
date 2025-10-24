stage('Run and Test') {
    steps {
        script {
            sh '''
                docker run --rm \
                    -e CELL_1=A1 \
                    -e CELL_2=H8 \
                    -e FIGURE=ферзь \
                    myapp:latest
            '''
        }
    }
}
