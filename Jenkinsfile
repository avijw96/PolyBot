pipeline {

    options{
    buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '5', numToKeepStr: '10'))
    disableConcurrentBuilds()
   }
    agent{
         docker{
              image 'jenkinsagent:latest'
              args  '--user root -v /var/run/docker.sock:/var/run/docker.sock'
         }
    }
    environment{
        SNYK_TOKEN = credentials('snyk-token')
    }
    stages {
       stage('Build Polyapp') {
               steps {
                 withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'pass', usernameVariable: 'user')]) {
                  sh "docker build -t avijwdocker/private-course:poly-bot-${env.BUILD_NUMBER} . "
                  sh "docker login --username $user --password $pass"
                    }
                }
            }
        stage('Test') {
            parallel {
                stage('pytest') {
                    steps {
                        withCredentials([file(credentialsId: 'telegramToken', variable: 'TELEGRAM_TOKEN')]) {
                        sh "cp ${TELEGRAM_TOKEN} .telegramToken"
                        sh 'pip3 install -r requirements.txt'
                        sh "python3 -m pytest --junitxml results.xml tests/*.py"
                        }
                    }
                }
                stage('pylint') {
                    steps {
                        script {
                            logs.info 'Start'
                            logs.warning 'you cant  do anything  '
                            sh "python3 -m pylint *.py || true"
                        }
                    }
                }
            }
        }

        stage('snyk test') {
            steps {
                sh "snyk container test --severity-threshold=critical avijwdocker/private-course:poly-bot-${env.BUILD_NUMBER} --file=Dockerfile"
            }
        }
        stage('push') {
            steps {
                    sh "docker push avijwdocker/private-course:poly-bot-${env.BUILD_NUMBER}"
                }
            }

        }

    }
