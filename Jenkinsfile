pipeline {
  agent any
  stages {
    stage('Check out repo') {
      steps {
        git(url: 'https://github.com/iRespectOnlyYen/Linguisage-Literature', branch: 'master')
      }
    }

    stage('Build') {
      steps {
        sh 'docker compose build'
      }
    }

    stage('Run') {
      steps {
        sh 'docker compose run'
      }
    }

  }
}