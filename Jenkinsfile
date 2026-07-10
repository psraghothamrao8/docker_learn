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
                docker { image 'python:3.9-slim' }
            }
            steps {
                echo 'Running python tests inside a python container...'
                sh 'pip install pytest && pytest'
            }
        }
        stage('Build Package') {
            steps {
                echo 'Building the final Docker image...'
                sh 'docker build -t simple-app .'
            }
        }
    }
}