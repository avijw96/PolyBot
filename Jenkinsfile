pipeline {
    options {
        // Configure build discarder using LogRotator strategy
        // Keep artifacts for 10 days and 10 builds
        buildDiscarder(logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '', daysToKeepStr: '5', numToKeepStr: '10'))
        // Disable concurrent builds
        disableConcurrentBuilds()
    }
    environment {
        // Set environment variable SNYK_TOKEN with the value from Jenkins credentials with ID 'snyk-token'
        SNYK_TOKEN = credentials('snyk-token')
    }
    agent {
        // Define agent as Docker container using 'jenkinsagent:latest' image
        // Mount Docker socket to allow Docker commands inside the container
        docker {
            image 'jenkinsagent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        // Define stages for the pipeline
        stage('Build Polyapp') {
            steps {
                // Use Jenkins credentials 'docker-hub-credentials' to login to Docker Hub
                // Build Docker image with tag avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh "docker build -t avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER} . "
                    sh "docker login --username $user --password $pass"
                }
            }
        }
        stage('Test') {
            // Define a parallel stage for testing
            parallel {
                stage('pylint') {
                    steps {
                        script {
                            // Run pylint on *.py files, ignoring errors to not fail the pipeline
                            sh "python3 -m pylint *.py || true"
                        }
                    }
                }
            }
        }
        stage('snyk test') {
            steps {
                // Use Jenkins credentials 'snyk-token' to set SNYK_TOKEN environment variable
                // Run Snyk container test with severity threshold set to 'high'
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    sh "snyk container test avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}--severity-threshold=high"
                }
            }
        }
        stage('push') {
            steps {
                // Push Docker image to Docker Hub
                sh "docker push avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
            }
        }
    }
}
