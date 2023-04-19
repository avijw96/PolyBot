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
                stage('pytest'){

                      steps {
                          withCredentials([string(credentialsId: 'telegramToken', variable: 'TELEGRAM_TOKEN')]) {
                             sh "touch .telegramToken"
                             sh "echo ${TELEGRAM_TOKEN} > .telegramToken"
                               sh "python3 -m pytest --junitxml results.xml tests/polytest.py"
                                     }
                                 }
                             }
               stage('pylint') {
                            steps {
                              script {
                                     sh "python3 -m pylint *.py || true"
                                     }
                               }//close steps
                           }//close stage pylint
                   }//close parallel
              }//close stage Test


        stage('push') {
            steps {
                    sh "docker push avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
                }
            }

        }

    }