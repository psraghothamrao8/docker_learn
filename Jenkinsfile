pipeline {
    agent any 

    triggers {
        // Check GitHub for new commits every single minute
        pollSCM('* * * * *')
    }

    stages {
        stage('Fetch Code') {
            steps {
                echo 'Pulling the latest code from GitHub...'
            }
        }
        stage('Run Tests') {
            agent {
                dockerfile {
                    filename 'Dockerfile.test'
                }
            }
            environment {
                // We securely pull the secret from Jenkins and give it to the test container
                SECRET_KEY = credentials('app-secret-key')
            }
            steps {
                echo 'Running tests against the active Jenkins secret key...'
                sh 'pytest'
            }
        }
        stage('Build Package') {
                    steps {
                        sh 'docker build -t simple-app:latest .'
                    }
        }
        /* stage('Deploy Locally') {
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
        } */

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Shipping image to Minikube container...'
                sh 'docker save simple-app:latest | docker exec -i minikube docker load'

                echo 'Locating and applying Kubernetes manifests inside the cluster...'
                sh '''
                    # The container finds its own internal kubectl path and executes it seamlessly
                    cat deployment.yaml | docker exec -i minikube /bin/bash -c '$(find /var/lib/minikube/binaries -name kubectl -type f | head -n 1) apply -f -'
                    
                    echo 'Checking deployment status...'
                    docker exec -i minikube /bin/bash -c '$(find /var/lib/minikube/binaries -name kubectl -type f | head -n 1) rollout status deployment/simple-app-deployment'
                '''
            }
        }

    }
    post {
        always {
            echo 'Cleaning up dangling Docker images to save space...'
            // Removes unused images without stopping your active container
            sh 'docker image prune -f'
        }
    }
}
