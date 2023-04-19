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
                stage('pthontest') {
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

        stage('push') {
            steps {
                    sh "docker push avijwdocker/olybot-aviyaaqov:poly-bot-${env.BUILD_NUMBER}"
                }
            }

        }

    }