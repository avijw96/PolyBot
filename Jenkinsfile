pipeline {
    options {
        buildDiscarder(logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10', daysToKeepStr: '5', numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    agent {
        docker {
            image 'jenkinsagent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Build Polyapp') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh "docker build -t avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER} . "
                    sh "docker login --username $user --password $pass"
                }
            }
        }

        stage('Test') {
            parallel {
                stage('pytest') {
                    steps {
                        catchError(message: 'pytest ERROR --> even this fails, we continue on', buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            withCredentials([file(credentialsId: 'telegramToken', variable: 'TELEGRAM_TOKEN')]) {
                                sh "cp ${TELEGRAM_TOKEN} .telegramToken"
                                sh 'pip3 install -r requirements.txt'
                                sh "python3 -m pytest --junitxml results.xml tests/*.py"
                            }
                        }
                    }
                }

                stage('pylint') {
                    steps {
                        catchError(message:'pylint ERROR',buildResult:'UNSTABLE',stageResult:'UNSTABLE'){
                            echo 'Starting'
                            echo 'Nothing to do!'
                            // Run pylint on *.py files, ignoring errors to not fail the pipeline
                            sh "python3 -m pylint *.py || true"
                        }
                    }
                }
            }
        }

        stage('Push') {
            steps {
                sh "docker push avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh 'export KUBECONFIG=${KUBECONFIG}'
                    sh 'kubectl apply -f app-deployment.yaml -n demoapp'
                }
            }
        }
    }
}
