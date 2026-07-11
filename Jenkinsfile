pipeline {
    agent any 
    
    stages {
        stage('Fetch Code') {
            steps {
                echo 'Pulling the latest code from GitHub...'
            }
        }
    stage('Run Tests') {
        agent {
            dockerfile { filename 'Dockerfile.test' }
        }
        steps {
            echo 'Running tests instantly using our pre-built tester image...'
            sh 'pytest' // No pip install needed! It runs instantly.
        }
    }
    stage('Build Package') {
                steps {
                    sh 'docker build -t simple-app:latest .'
                }
            }
    stage('Deploy Locally') {
            environment {
                // This securely extracts your secret from Jenkins credentials
                REAL_SECRET = credentials('app-secret-key')
            }
            steps {
                echo 'Deploying app to Ubuntu with injected secrets...'
                sh 'docker stop my-running-app || true'
                sh 'docker rm my-running-app || true'
                
                // Note the double quotes "" instead of single quotes so Jenkins can swap the variable
                sh "docker run -d --name my-running-app -p 8081:5000 -e SECRET_KEY='${REAL_SECRET}' simple-app:latest"
            }
        }
    }
}
