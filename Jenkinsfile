pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Building DNS project...'

                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'

                echo 'Build completed successfully.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'

                bat 'python -m pytest -v'

                echo 'All tests completed.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}