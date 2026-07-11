// The root element defining a declarative Jenkins CI/CD (Continuous Integration/Continuous Delivery) pipeline.
pipeline {
    // Instructs Jenkins to run the pipeline steps on any available build agent/executor.
    agent any 

    // Define triggers to automate starting this pipeline on events.
    triggers {
        // Poll Source Control Management (SCM) like GitHub every single minute (* * * * *) for new commits.
        // If a new commit is pushed to GitHub, Jenkins will automatically start a new build.
        pollSCM('* * * * *')
    }

    // The stages block contains a sequence of tasks (stages) to run during the build process.
    stages {
        
        // Stage 1: Fetch the latest code from SCM (GitHub/Git).
        stage('Fetch Code') {
            steps {
                // Print a progress message to the Jenkins build console logs.
                echo 'Pulling the latest code from GitHub...'
            }
        }
        
        // Stage 2: Spin up a test environment container and execute pytest tests.
        stage('Run Tests') {
            // This stage runs inside a Docker container built dynamically on-the-fly using 'Dockerfile.test'.
            // This ensures our test runner environment is clean and identical on every build.
            agent {
                dockerfile {
                    filename 'Dockerfile.test'
                }
            }
            // Injected environment variables for this specific stage.
            environment {
                // Retrieve the credential with ID 'app-secret-key' securely from Jenkins Credentials Manager
                // and bind its value to the environment variable 'SECRET_KEY' so pytest can read it.
                // This keeps sensitive secrets out of our code repositories!
                SECRET_KEY = credentials('app-secret-key')
            }
            steps {
                echo 'Running tests against the active Jenkins secret key...'
                // Run the pytest testing tool inside our temporary test container.
                // 'sh' executes shell commands on the agent.
                sh 'pytest'
            }
        }
        
        // Stage 3: Build the production Docker image.
        stage('Build Package') {
            steps {
                // Build a Docker image named 'simple-app' tagged as 'latest' using the production 'Dockerfile'.
                // This image will represent our packaged web application.
                sh 'docker build -t simple-app:latest .'
            }
        }
        
        // Stage 3.5: Deploy Locally (Uncommented to ensure local Docker container gets updated)
        stage('Deploy Locally') {
                environment {
                    // This securely extracts your secret from Jenkins credentials
                    REAL_SECRET = credentials('app-secret-key')
                }
                steps {
                    echo 'Deploying app to local Docker container with injected secrets...'
                    sh 'docker stop my-running-app || true'
                    sh 'docker rm my-running-app || true'
                    
                    // Note the double quotes "" instead of single quotes so Jenkins can swap the variable
                    sh "docker run -d --name my-running-app -p 8081:5000 -e SECRET_KEY='${REAL_SECRET}' simple-app:latest"
                }
        } 

        // Stage 4: Deploy the application to our local Kubernetes (Minikube) cluster.
        stage('Deploy to Kubernetes') {
            environment {
                // Fetch the secret key from Jenkins credentials manager.
                LIVE_SECRET = credentials('app-secret-key')
            }
            steps {
                echo 'Shipping image to Minikube container...'
                
                // Explain this command:
                // 1. 'docker save simple-app:latest' packages our built image into a tar stream.
                // 2. The pipe '|' sends that stream directly to Minikube's Docker daemon.
                // 3. 'docker exec -i minikube docker load' extracts it inside Minikube.
                // This is a neat trick to share local images with Minikube without using an external Docker Registry.
                sh 'docker save simple-app:latest | docker exec -i minikube docker load'

                echo 'Locating cluster binaries and generating secure keys...'
                
                // We use a multi-line shell script to setup Kubernetes secrets and apply manifests.
                sh '''
                    # 1. Locate the exact filepath of the 'kubectl' command-line binary inside Minikube.
                    # We find it dynamically and strip any hidden carriage returns (\\r) using 'tr'.
                    KUBECTL_BIN=$(docker exec minikube find /var/lib/minikube/binaries -name kubectl -type f | head -n 1 | tr -d '\\r')
                    echo "Found cluster kubectl binary at: ${KUBECTL_BIN}"
                    
                    # 2. Create or update the Kubernetes Secret resource dynamically.
                    # - 'export KUBECONFIG=...' tells kubectl where to find cluster admin configuration files inside Minikube.
                    # - 'create secret generic app-secret --from-literal=secret-key=${LIVE_SECRET} --dry-run=client -o yaml' 
                    #   generates a secret payload in memory without actually applying it.
                    # - '| ${KUBECTL_BIN} apply -f -' pipes that generated payload into the apply command.
                    # This lets us create or update the secret in a single step without getting "already exists" errors.
                    docker exec -i minikube /bin/bash -c "export KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf && ${KUBECTL_BIN} create secret generic app-secret --from-literal=secret-key=${LIVE_SECRET} --dry-run=client -o yaml | ${KUBECTL_BIN} apply -f -"
                    
                    # 3. Apply the updated Kubernetes deployment manifest.
                    # We pipe the contents of 'deployment.yaml' from our workspace directly into Minikube's kubectl.
                    cat deployment.yaml | docker exec -i minikube /bin/bash -c "export KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf && ${KUBECTL_BIN} apply -f -"
                    
                    # 4. Force a restart of the Kubernetes deployment.
                    # Since the image is tagged as 'latest' and imagePullPolicy is 'Never', Kubernetes
                    # won't automatically recreate the pods if the deployment.yaml manifest itself is unchanged.
                    # This rollout restart command forces Kubernetes to terminate the old pods and launch new ones with the new image.
                    docker exec -i minikube /bin/bash -c "export KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf && ${KUBECTL_BIN} rollout restart deployment/simple-app-deployment"
                    
                    # 5. Monitor rollout status to verify the pods deploy successfully.
                    # This command will block and wait until the replicas are fully started and healthy.
                    docker exec -i minikube /bin/bash -c "export KUBECONFIG=/root/.kube/config:/etc/kubernetes/admin.conf && ${KUBECTL_BIN} rollout status deployment/simple-app-deployment"
                '''
            }
        }
    }
    
    // Actions that execute after the main stages complete.
    post {
        always {
            echo 'Cleaning up dangling Docker images to save space...'
            // Clean up unused/dangling docker resources on the build server.
            // This prevents the host machine from running out of disk space due to intermediate build cache layers.
            sh 'docker image prune -f'
        }
    }
}
