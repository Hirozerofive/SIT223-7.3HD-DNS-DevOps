pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\hiruk\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        DOCKER = 'C:\\Users\\hiruk\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE_NAME = 'simple-dns'
        CONTAINER_NAME = 'simple-dns-container'
    }

    stages {

        stage('Build') {
            steps {
                echo '===== BUILD STAGE ====='

                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip install -r requirements.txt'

                bat '"%DOCKER%" build -t %IMAGE_NAME%:%BUILD_NUMBER% .'

                echo 'Docker image built successfully.'
            }
        }

        stage('Test') {
            steps {
                echo '===== TEST STAGE ====='

                bat '"%PYTHON%" -m pytest -v'

                echo 'All automated tests passed.'
            }
        }

        stage('Code Quality') {
            steps {
                echo '===== CODE QUALITY STAGE ====='

                bat '"%PYTHON%" -m pylint dns.py --exit-zero'

                echo 'Code quality analysis completed.'
            }
        }

        stage('Security') {
            steps {
                echo '===== SECURITY STAGE ====='

                bat '"%PYTHON%" -m bandit -r dns.py client.py'

                echo 'Security scan completed.'
            }
        }

        stage('Deploy') {
            steps {
                echo '===== DEPLOY STAGE ====='

                bat '"%DOCKER%" rm -f %CONTAINER_NAME% 2>nul || exit /b 0'

                bat '"%DOCKER%" run -d --name %CONTAINER_NAME% -p 5000:5000/udp %IMAGE_NAME%:%BUILD_NUMBER%'

                echo 'Application deployed successfully.'
            }
        }

        stage('Release') {
            steps {
                echo '===== RELEASE STAGE ====='

                bat '"%DOCKER%" tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:release-%BUILD_NUMBER%'

                bat '"%DOCKER%" images %IMAGE_NAME%'

                echo 'Versioned release created successfully.'
            }
        }

        stage('Monitoring') {
            steps {
                echo '===== MONITORING STAGE ====='

                bat 'timeout /t 3 /nobreak'

                bat '"%DOCKER%" ps --filter "name=%CONTAINER_NAME%"'

                bat '"%PYTHON%" health_check.py'

                echo 'Monitoring health check passed.'
            }
        }
    }

    post {
        success {
            echo '======================================'
            echo 'DEVOPS PIPELINE COMPLETED SUCCESSFULLY!'
            echo 'All 7 stages passed.'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'PIPELINE FAILED!'
            echo 'Check the failed stage in Jenkins.'
            echo '======================================'
        }

        always {
            echo "Pipeline finished for Jenkins Build #${BUILD_NUMBER}"
        }
    }
}