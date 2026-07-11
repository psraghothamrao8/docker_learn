// The root element defining a declarative Jenkins CI/CD pipeline
pipeline {
    // Instructs Jenkins to run the pipeline steps on any available build agent/executor
    agent any 

    // Define triggers to automate starting this pipeline
    triggers {
        // Poll Source Control Management (SCM) like GitHub every single minute (* * * * *) for new commits.
        // If a new commit is detected, Jenkins will automatically start a new build.
        pollSCM('* * * * *')
    }

    // The stages block contains a sequence of tasks (stages) to run during the build
    stages {
        
        // Stage 1: Fetch the latest code from SCM (GitHub/Git)
        stage('Fetch Code') {
            steps {
                // Print a progress message to the Jenkins build console logs
                echo 'Pulling the latest code from GitHub...'
            }
        }
        
        // Stage 2: Spin up a test environment container and execute pytest tests
        stage('Run Tests') {
            // This stage runs inside a Docker container built dynamically using Dockerfile.test
            agent {
                dockerfile {
                    filename 'Dockerfile.test'
                }
            }
            // Injected environment variables for this specific stage
            environment {
                // Retrieve the credential with ID 'app-secret-key' securely from Jenkins Credentials Manager
                // and bind its value to the environment variable SECRET_KEY so pytest can read it
                SECRET_KEY = credentials('app-secret-key')
            }
            steps {
                echo 'Running tests against the active Jenkins secret key...'
                // Run the pytest testing tool inside our test container
                sh 'pytest'
            }
        }
        
        // Stage 3: Build the production Docker image
        stage('Build Package') {
            steps {
                // Build a Docker image named 'simple-app' tagged as 'latest' using the production 'Dockerfile'
                sh 'docker build -t simple-app:latest .'
            }
        }
        
        /* 
        // Commented out Stage: Deploy Locally (Left here for reference/alternative setups)
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
        */

        // Stage 4: Deploy the containerized application onto the Kubernetes cluster
        stage('Deploy to Kubernetes') {
            environment {
                // Securely fetch your production secret from the Jenkins credentials manager
                LIVE_SECRET = credentials('app-secret-key')
            }
            steps {
                echo 'Shipping image to Minikube container...'
                sh 'docker save simple-app:latest | docker exec -i minikube docker load'

                echo 'Locating cluster binaries and generating secure keys...'
                sh '''
                    KUBECTL_BIN=$(docker exec minikube find /var/lib/minikube/binaries -name kubectl -type f | head -n 1 | tr -d '\\r')
                    
                    # 1. Securely generate/update the secret inside Kubernetes using the Jenkins vault value
                    docker exec -i minikube /bin/bash -c "KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf ${KUBECTL_BIN} create secret generic app-secret --from-literal=secret-key=${LIVE_SECRET} --dry-run=client -o yaml | ${KUBECTL_BIN} apply -f -"
                    
                    # 2. Apply your updated deployment manifest
                    cat deployment.yaml | docker exec -i minikube /bin/bash -c "KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf ${KUBECTL_BIN} apply -f -"
                    
                    # 3. Track rollout status
                    docker exec -i minikube /bin/bash -c "KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf ${KUBECTL_BIN} rollout status deployment/simple-app-deployment"
                '''
            }
        }

    }
    
    // Actions that run post-pipeline execution
    post {
        always {
            echo 'Cleaning up dangling Docker images to save space...'
            // Clean up unused/dangling docker resources on the build server (untagged intermediate build layers)
            sh 'docker image prune -f'
        }
    }
}

