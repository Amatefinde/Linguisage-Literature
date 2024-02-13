pipeline {
  agent any
  stages {
    stage('Check out repo') {
      steps {
        git(url: 'https://github.com/iRespectOnlyYen/Linguisage-Literature', branch: 'master')
      }
    }

    stage('Log files') {
      steps {
        sh 'ls -la'
      }
    }

  }
}