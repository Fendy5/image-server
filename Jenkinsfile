pipeline {
  agent any
  stages {
    stage('Git Pull') {
      steps {
        git(credentialsId: 'e39944bd-4ff3-4755-a758-2b23ac136fc6', branch: 'main', url: "git@github.com:Fendy5/${env.ItemName}-server.git")
      }
    }

    stage('Build') {
      steps {
        sh "docker buildx build --progress=plain -t common-services-${env.ItemName} ."
      }
    }

    stage('Deploy') {
      steps {
        script{
          try {
            sh "docker stop common-services-${env.ItemName}"
            sh "docker rm common-services-${env.ItemName}"
          } catch(Exception e) {
            echo "命令执行出错: ${e.getMessage()}"
          }
          sh "docker run -it -d --restart=always --ip 172.17.0.5 --name common-services-${env.ItemName} -v /www/wwwroot/${env.ItemName}.server/media:/app/media -v /www/wwwroot/${env.ItemName}.server/logs:/app/logs -p 7015:8000 common-services-${env.ItemName}"
          sh "docker image prune -f"
        }
      }
    }
  }
  environment {
    ItemName = 'image'
  }
  options {
    skipDefaultCheckout(true)
  }
}
