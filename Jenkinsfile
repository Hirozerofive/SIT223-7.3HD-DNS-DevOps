pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\hiruk\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building DNS project...'

                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip install -r requirements.txt'

                echo 'Build completed successfully.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'

                bat '"%PYTHON%" -m pytest -v'

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