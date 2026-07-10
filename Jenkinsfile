pipeline {
    agent any 
    
    stages {
        stage('Fetch Code') {
            steps {
                echo 'Pulling the latest code from GitHub...'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running python tests...'
                // Inside Jenkins, we use 'sh' or 'bat' to run commands
                sh 'pip install pytest && pytest'
            }
        }
        stage('Build Package') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t simple-app .'
            }
        }
    }
}