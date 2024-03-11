#!groovy

def isPullRequest = env.CHANGE_ID ? true : false

pipeline {

  agent {
    label 'dream'
  }
  environment {
    WAIT_TIMEOUT=2400
    WAIT_INTERVAL=10
    COMPOSE_HTTP_TIMEOUT=120
  }
  stages {
    stage('Checkout') {
      steps {
        script {
          def branch = "Current branch is ${env.BRANCH_NAME}"
          if (isPullRequest) {
            echo """${branch}
            Git commiter name: ${env.GIT_AUTHOR_NAME} or ${env.GIT_COMMITTER_NAME}
            Pull request: merge ${env.CHANGE_BRANCH} into ${env.CHANGE_TARGET}
            Pull request id: ${pullRequest.id} or ${env.CHANGE_ID}
            Pull request title: ${pullRequest.title}
            Pull request headRef: ${pullRequest.headRef}
            Pull request base: ${pullRequest.base}
            """
          }
          else {
            echo "${branch}"
          }
        }
      }
    }
// ------------------------------------------- Test prompted dists------------------------------------------------
    stage('Build-MGPT35') {
      steps {
        script{
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh '''
                cat /home/ignatov/secrets.txt >> .env_secret
                tests/runtests_multiskill_davinci3.sh MODE=build
              '''
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        aborted {
          script {
            sh 'tests/runtests_multiskill_davinci3.sh MODE=clean'
          }
        }
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }
    stage('Start-MGPT35') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests_multiskill_davinci3.sh MODE=clean && tests/runtests_multiskill_davinci3.sh MODE=start'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            started = true
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_multiskill_davinci3.sh MODE=clean'
          }
        }
      }
    }
    stage('Test skills-MGPT35') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh label: 'test skills', script: 'tests/runtests_multiskill_davinci3.sh MODE=test_skills'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_multiskill_davinci3.sh MODE=clean'
          }
        }
      }
    }
// ------------------------------------------- Test prompted dists------------------------------------------------
    stage('Build-MGPTJT') {
      steps {
        script{
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh '''
                cat /home/ignatov/secrets.txt >> .env_secret
                tests/runtests_multiskill_davinci3.sh MODE=clean
                tests/runtests_marketing_gptjt.sh MODE=build
              '''
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        aborted {
          script {
            sh 'tests/runtests_marketing_gptjt.sh MODE=clean'
          }
        }
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }
    stage('Start-MGPTJT') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests_marketing_gptjt.sh MODE=clean && tests/runtests_marketing_gptjt.sh MODE=start'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            started = true
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_marketing_gptjt.sh MODE=clean'
          }
        }
      }
    }
    stage('Test skills-MGPTJT') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh label: 'test skills', script: 'tests/runtests_marketing_gptjt.sh MODE=test_skills'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_marketing_gptjt.sh MODE=clean'
          }
        }
      }
    }
// ------------------------------------------- Test prompted dists------------------------------------------------
    stage('Build-DCGPT') {
      steps {
        script{
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh '''
                cat /home/ignatov/secrets.txt >> .env_secret
                tests/runtests_marketing_gptjt.sh MODE=clean
                tests/runtests_deeppavlov_chatgpt.sh MODE=build
              '''
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        aborted {
          script {
            sh 'tests/runtests_deeppavlov_chatgpt.sh MODE=clean'
          }
        }
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }
    stage('Start-DCGPT') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests_deeppavlov_chatgpt.sh MODE=clean && tests/runtests_deeppavlov_chatgpt.sh MODE=start'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            started = true
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_deeppavlov_chatgpt.sh MODE=clean'
          }
        }
      }
    }
    stage('Test skills-DCGPT') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh label: 'test skills', script: 'tests/runtests_deeppavlov_chatgpt.sh MODE=test_skills'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_deeppavlov_chatgpt.sh MODE=clean'
          }
        }
      }
    }
// ------------------------------------------- Test prompted dists------------------------------------------------
    stage('Build-NOASST') {
      steps {
        script{
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh '''
                cat /home/ignatov/secrets.txt >> .env_secret
                tests/runtests_deeppavlov_chatgpt.sh MODE=clean
                tests/runtests_nutrition_oasst.sh MODE=build
              '''
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        aborted {
          script {
            sh 'tests/runtests_nutrition_oasst.sh MODE=clean'
          }
        }
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }
    stage('Start-NOASST') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests_nutrition_oasst.sh MODE=clean && tests/runtests_nutrition_oasst.sh MODE=start'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            started = true
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_nutrition_oasst.sh MODE=clean'
          }
        }
      }
    }
    stage('Test skills-NOASST') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh label: 'test skills', script: 'tests/runtests_nutrition_oasst.sh MODE=test_skills'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_nutrition_oasst.sh MODE=clean'
          }
        }
      }
    }
// ------------------------------------------- Test dream dist------------------------------------------------
    stage('Build') {
      steps {
        script{
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh '''
                cat /home/ignatov/secrets.txt >> .env
                tests/runtests_nutrition_oasst.sh MODE=clean
                tests/runtests.sh MODE=build
              '''
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        aborted {
          script {
            sh 'tests/runtests.sh MODE=clean'
          }
        }
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }

    stage('Start') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests.sh MODE=clean && tests/runtests.sh MODE=start'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            started = true
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests.sh MODE=clean'
          }
        }
      }
    }

    stage('Test dialog') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests.sh MODE=test_dialog'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }

    stage('Test skills') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh label: 'test skills', script: 'tests/runtests.sh MODE=test_skills'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests.sh MODE=clean'
          }
        }
      }
    }

// ------------------------------------------- Test Ru dream dist------------------------------------------------
    stage('Build-RU') {
      steps {
        script{
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh '''
                cat /home/ignatov/secrets.txt >> .env_ru
                tests/runtests.sh MODE=clean
                tests/runtests_russian.sh MODE=build
              '''
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        aborted {
          script {
            sh 'tests/runtests_russian.sh MODE=clean'
          }
        }
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
      }
    }

    stage('Start-RU') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh 'tests/runtests_russian.sh MODE=clean && tests/runtests_russian.sh MODE=start'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            started = true
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_russian.sh MODE=clean'
          }
        }
      }
    }

    stage('Test skills-RU') {
      steps {
        script {
          startTime = currentBuild.duration
          Exception ex = null
          catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
            try {
              sh label: 'test skills', script: 'tests/runtests_russian.sh MODE=test_skills'
            }
            catch (Exception e) {
              int duration = (currentBuild.duration - startTime) / 1000
              throw e
            }
          }
        }
      }
      post {
        success {
          script {
            int duration = (currentBuild.duration - startTime) / 1000
          }
        }
        aborted {
          script {
            sh 'tests/runtests_russian.sh MODE=clean'
          }
        }
      }
    }


  }
  post {
    aborted {
      script {
        sh 'aborted'
      }
    }
    cleanup {
      script {
        if (started) {
          sh './tests/runtests_multiskill_davinci3.sh MODE=clean'
          sh './tests/runtests_marketing_gptjt.sh MODE=clean'
          sh './tests/runtests_nutrition_oasst.sh MODE=clean'
          sh './tests/runtests_deeppavlov_chatgpt.sh MODE=clean'
          sh './tests/runtests.sh MODE=clean'
          sh './tests/runtests_russian.sh MODE=clean'
          sh './tests/runtests_multilingual.sh MODE=clean'
        }
      }
    }
  }
}
