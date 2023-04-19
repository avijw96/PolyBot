pipeline {

    options{
    buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '5', numToKeepStr: '10'))
    disableConcurrentBuilds()
   }
    environment{
        SNYK_TOKEN = credentials('snyk-token')
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
        parallel{

               stage('pylint') {
                            steps {
                              script {
                                     sh "python3 -m pylint *.py || true"
                                     }
                               }//close steps
                           }//close stage pylint
                   }//close parallel
              }//close stage Test
       stage('snyk test') {
            steps {
                sh "snyk container test avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}--severity-threshold=high"
             }
           }
        stage('push') {
            steps {
                    sh "docker push avijwdocker/polybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
                }
            }

        }

    }