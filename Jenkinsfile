pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\hiruk\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        IMAGE_NAME = 'simple-dns'
        CONTAINER_NAME = 'simple-dns-container'
    }

    stages {

        // 1. BUILD
        stage('Build') {
            steps {
                echo '===== BUILD STAGE ====='

                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip install -r requirements.txt'

                // Build Docker image
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'

                echo 'Docker image built successfully.'
            }
        }

        // 2. TEST
        stage('Test') {
            steps {
                echo '===== TEST STAGE ====='

                bat '"%PYTHON%" -m pytest -v'

                echo 'All automated tests passed.'
            }
        }

        // 3. CODE QUALITY
        stage('Code Quality') {
            steps {
                echo '===== CODE QUALITY STAGE ====='

                bat '"%PYTHON%" -m pylint dns.py --exit-zero'

                echo 'Code quality analysis completed.'
            }
        }

        // 4. SECURITY
        stage('Security') {
            steps {
                echo '===== SECURITY STAGE ====='

                bat '"%PYTHON%" -m bandit -r dns.py client.py'

                echo 'Security scan completed.'
            }
        }

        // 5. DEPLOY
        stage('Deploy') {
            steps {
                echo '===== DEPLOY STAGE ====='

                // Remove previous container if it exists
                bat 'docker rm -f %CONTAINER_NAME% 2>nul || exit /b 0'

                // Deploy new version
                bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000/udp %IMAGE_NAME%:%BUILD_NUMBER%'

                echo 'Application deployed successfully.'
            }
        }

        // 6. RELEASE
        stage('Release') {
            steps {
                echo '===== RELEASE STAGE ====='

                // Create versioned release tag
                bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:release-%BUILD_NUMBER%'

                echo 'Release image created.'
                bat 'docker images %IMAGE_NAME%'
            }
        }

        // 7. MONITORING
        stage('Monitoring') {
            steps {
                echo '===== MONITORING STAGE ====='

                // Give container a few seconds to start
                bat 'timeout /t 3 /nobreak'

                // Check that container is running
                bat 'docker ps --filter "name=%CONTAINER_NAME%"'

                // Application health check
                bat '"%PYTHON%" health_check.py'

                echo 'Monitoring health check passed.'
            }
        }
    }

    post {

        success {
            echo '======================================'
            echo 'DEVOPS PIPELINE COMPLETED SUCCESSFULLY!'
            echo 'Build, Test, Quality, Security, Deploy, Release and Monitoring passed.'
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