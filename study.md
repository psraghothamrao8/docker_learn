# The DevOps Handbook: Docker, Jenkins, & Kubernetes Study Guide

Welcome to your learning guide! This document breaks down the core theoretical concepts you encountered in this project. It is structured to help you understand the *what*, *why*, and *how* of modern containerized application deployment.

---

## Table of Contents
1. [The Big Picture: What is CI/CD & DevOps?](#1-the-big-picture-what-is-cicd--devops)
2. [Docker: Containerization Basics](#2-docker-containerization-basics)
3. [Jenkins: The Orchestrator of Automation (CI/CD)](#3-jenkins-the-orchestrator-of-automation-cicd)
4. [Kubernetes: Container Orchestration](#4-kubernetes-container-orchestration)
5. [The Integration Workflow: How It All Fits Together](#5-the-integration-workflow-how-it-all-fits-together)

---

## 1. The Big Picture: What is CI/CD & DevOps?

Historically, software developers wrote code on their machines, and when finished, passed it to a separate Operations team to deploy it. This created the infamous **"It works on my machine"** problem due to differences in database versions, operating systems, and environment setups.

**DevOps** is a set of practices that combines Software Development (**Dev**) and IT Operations (**Ops**). The goal is to shorten the systems development life cycle and provide continuous delivery with high software quality.

### What is CI/CD?
```
[Code Commit] ──► [Continuous Integration (CI)] ──► [Continuous Deployment (CD)] ──► [Live App]
                      (Build & Run Tests)               (Deploy to Kubernetes)
```

*   **Continuous Integration (CI):** The practice of automating the integration of code changes from multiple contributors into a single software project. 
    *   *What it does:* Every time you save/commit code, automated systems pull the code, compile it, and run tests.
    *   *Why it matters:* Catches bugs within minutes of writing them, rather than weeks later.
*   **Continuous Delivery / Deployment (CD):** 
    *   **Delivery:** Automatically prepares code changes for a release to production, but requires a manual click to deploy.
    *   **Deployment:** Automatically deploys every validated change directly to production without human intervention.

---

## 2. Docker: Containerization Basics

### What is Containerization?
Imagine you are shipping cargo. In the past, goods were loaded loose on ships—crates of food next to heavy machinery. Things got crushed, contaminated, or lost. Then came **Standard Shipping Containers**. Every ship, crane, and truck is built to handle the exact same size container, regardless of what is inside.

In software, **Docker** is that shipping container. It packages your code and *every single thing* your code needs to run (Python, libraries, system files) into a single box.

| Feature | Virtual Machines (VMs) | Docker Containers |
| :--- | :--- | :--- |
| **Architecture** | Includes a full guest Operating System (OS). | Shares the host machine's Operating System kernel. |
| **Weight** | Heavy (Gigabytes, slow startup). | Extremely lightweight (Megabytes, near-instant startup). |
| **Efficiency** | High resource overhead. | Very low resource overhead. |

### Core Docker Terms You Must Know
1.  **Dockerfile:** A recipe text file containing step-by-step instructions on how to build a container image.
2.  **Image:** The static "blueprint" or read-only package created by building a Dockerfile. Think of it as a class in programming, or a zip file containing the entire environment.
3.  **Container:** A live, running instance of an Image. Think of it as an object created from a class, or the unzipped, running program.
4.  **Docker Host Socket (`docker.sock`):** The Unix socket that the Docker daemon listens to. Mounting this inside a container (like Jenkins) allows that container to speak to your computer's Docker system and launch *other* containers.

### Crucial Dockerfile Instructions
*   `FROM`: Defines the starting base image (e.g., `python:3.9-slim`).
*   `WORKDIR`: Creates and sets the active working directory inside the container.
*   `RUN`: Executes commands *during the build process* (e.g., installing packages with `pip install`).
*   `COPY`: Copies files from your local computer into the container filesystem.
*   `CMD`: Specifies the default command that executes *only when a container is started*.

---

## 3. Jenkins: The Orchestrator of Automation (CI/CD)

**Jenkins** is an open-source automation server. It acts as the "manager" of your project. Whenever code changes, Jenkins wakes up, reads your instructions, and runs them.

### Jenkins Pipelines
We use **Declarative Pipelines** (configured via a file named `Jenkinsfile`) to write our automation workflow. 

```groovy
pipeline {
    agent any // Tells Jenkins WHERE to run (any machine with a Jenkins agent)
    stages {
        stage('Example') { // A major phase of the build (e.g. Test, Build, Deploy)
            steps {
                echo 'Hello World' // The actual commands executed
            }
        }
    }
}
```

### Core Jenkins Concepts
*   **Agent:** The machine or environment where the build steps run. In our `Run Tests` stage, we set the agent to a `dockerfile` (`Dockerfile.test`). This tells Jenkins: *"Spin up a container using this test recipe, run the pytest command inside it, and throw the container away when done."*
*   **Triggers / PollSCM:** Configures Jenkins to constantly check your repository (e.g. GitHub) at regular intervals (like every minute) to see if you pushed new code. If it detects a change, it automatically triggers a build run.
*   **Credentials Binding:** Secrets (like passwords or API keys) should *never* be written directly in code. Jenkins has a secure database. We register a credential there under an ID (like `app-secret-key`) and inject it into the pipeline's environment block as a variable (`SECRET_KEY = credentials(...)`).

---

## 4. Kubernetes: Container Orchestration

If Docker runs individual containers, **Kubernetes (K8s)** is the conductor of an entire orchestra of containers. It manages thousands of containers across multiple servers, scaling them up or down, and auto-healing them if they crash.

### Core Kubernetes Resources
```
       [ Kubernetes Service (Load Balancer / NodePort) ]
                      /                 \
                     /                   \
        [ Pod Replica 1 ]             [ Pod Replica 2 ]
        (Container: App)              (Container: App)
```

1.  **Pod:** The smallest deployable unit in Kubernetes. A Pod holds one or more containers (usually just one) that share network and storage resources.
2.  **Deployment:** A manager that describes the *desired state* for your Pods. For example: *"I want exactly 2 replicas of the simple-app container running at all times."* If one Pod crashes, the Deployment immediately detects it and starts a new one automatically.
3.  **Service:** Since Pods are frequently destroyed and recreated, their internal IP addresses constantly change. A **Service** provides a stable network address (IP and port) that routes incoming traffic to the active Pods.
    *   *NodePort:* Exposes the service on a static port on each Node (server) IP. This is how we access our Minikube deployment from our computer browser (`nodePort: 30080`).
4.  **Secret:** An object that stores sensitive data, such as passwords or keys. Kubernetes mounts these secrets securely into container environment variables without displaying them in configuration files.

### Crucial K8s Concepts
*   **Desired State vs. Actual State:** You tell Kubernetes what you *want* (e.g., "Run 3 pods"). Kubernetes constantly loops, checks the actual state of the cluster, and automatically takes action to correct any mismatch.
*   **ImagePullPolicy (Never):** Tells Kubernetes not to check external websites (like Docker Hub) for the container image, but instead to use the local container image already built and stored in Minikube's internal Docker registry.

---

## 5. The Integration Workflow: How It All Fits Together

Here is the exact lifecycle of a code change in this project:

```
[Developer Machine]
       │
       ▼ (Code Commit / Push)
[GitHub Repository]
       │
       ▼ (PollSCM detects commit every minute)
[Jenkins Server]
       │
       ├─► 1. Spins up Docker Test Container (Dockerfile.test)
       ├─► 2. Inject environment secret -> Runs pytest tests inside
       ├─► 3. If tests pass, builds production Docker Image (Dockerfile)
       │
       ▼ (Deploy to Kubernetes Phase)
[Minikube Cluster (K8s)]
       │
       ├─► 1. Loads production image into its local container cache
       ├─► 2. Generates K8s secret securely from Jenkins Credential
       ├─► 3. Applies deployment.yaml manifest
       ├─► 4. Kubernetes starts Pod replicas & Service routes traffic
```

This ensures that:
*   No untested code goes to production.
*   Production configuration remains secure and automated.
*   The application stays up and load-balanced automatically.
