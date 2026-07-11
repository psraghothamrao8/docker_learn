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
        steps {
            echo 'Deploying app to Ubuntu...'
            // 1. Stop and remove the old version if it's already running
            sh 'docker stop my-running-app || true'
            sh 'docker rm my-running-app || true'
            
            // 2. Start the fresh image we just built
            sh 'docker run -d --name my-running-app -p 8081:5000 simple-app:latest'
        }
    }
    }
}
