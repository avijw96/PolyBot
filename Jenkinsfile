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
                sstage('pytest'){
                        steps{
                        catchError(message:'pytest ERROR-->even this fails,we continue on',buildResult:'UNSTABLE',stageResult:'UNSTABLE'){
                        withCredentials([file(credentialsId: 'telegramToken', variable: 'TOKEN_FILE')]) {
                            sh "cp ${TOKEN_FILE} ./.telegramToken"
                            sh 'pip3 install --no-cache-dir -r requirements.txt'
                            sh 'python3 -m pytest --junitxml results.xml tests/*.py'
                                     }//close Credentials
                                 }//close catchError
                             }//close steps
                        }//close stage pytest

               stage('pylint') {
                         steps {
                         catchError(message:'pylint ERROR-->even this fails,we continue on',buildResult:'UNSTABLE',stageResult:'UNSTABLE'){
                              script {

                                     sh "python3 -m pylint *.py || true"
                                     }
                                  }//close catchError
                               }//close steps
                           }//close stage pylint
                   }//close parallel
              }//close stage Test


        stage('push') {
            steps {
                    sh "docker push avijwdocker/olybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
                }
            }

        }

    }