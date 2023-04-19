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


        stage('push') {
            steps {
                    sh "docker push avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
                }
            }

        }

    }