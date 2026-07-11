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
                echo 'Tests passed! Building the final production image...'
                sh 'docker build -t simple-app .'
            }
        }
    }
}
