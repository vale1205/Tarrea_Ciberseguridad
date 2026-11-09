pipeline {
    agent any
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }
    environment {
        PIPENV_VENV_IN_PROJECT = '1'
        PIPENV_IGNORE_VIRTUALENVS = '1'
        PIPENV_NOSPIN = '1'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    env.GIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    env.APP_VERSION = "1.0.${env.BUILD_NUMBER}+${env.GIT_SHA}"
                }
                sh 'mkdir -p reports && pipenv sync --dev'
                sh 'pipenv run python -m compileall -q app.py'
            }
        }
        stage('Test') {
            steps { sh 'pipenv run pytest --junitxml=reports/junit.xml' }
            post { always { junit testResults: 'reports/junit.xml', allowEmptyResults: true } }
        }
        stage('Generate Documentation') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
set -euo pipefail
rm -rf docs/html
mkdir -p reports
rm -f reports/doxygen_warnings.log
doxygen Doxyfile
test -s docs/html/index.html
if [ -s reports/doxygen_warnings.log ]; then
    cat reports/doxygen_warnings.log
    exit 1
fi
echo 'Documentación generada sin advertencias'
'''
                }
            }
            post { always { archiveArtifacts artifacts: 'docs/html/**', allowEmptyArchive: true } }
        }
        stage('Version Control') {
            when { expression { currentBuild.currentResult == 'SUCCESS' } }
            steps {
                sh 'bash scripts/trazabilidad.sh'
                script {
                    // El laboratorio utiliza un remoto local. Para GitHub se usa una credencial de Jenkins.
                    def remote = sh(returnStdout: true, script: 'git remote get-url origin').trim()
                    if (remote.startsWith('/repos/')) {
                        sh 'bash scripts/versionar_docs.sh'
                    } else {
                        withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                            sh 'bash scripts/versionar_docs.sh'
                        }
                    }
                }
            }
        }
        stage('Deploy') {
            when { expression { currentBuild.currentResult == 'SUCCESS' } }
            steps { sh 'bash scripts/deploy_test.sh' }
        }
    }
    post {
        always { archiveArtifacts artifacts: 'reports/**,docs/TRAZABILIDAD.md', allowEmptyArchive: true }
        unstable { echo 'ALERTA: documentación incompleta. Revisar reports/doxygen_warnings.log. No se versiona ni despliega.' }
        failure { echo 'ALERTA: pipeline fallido. Revisar Console Output y los informes archivados.' }
        success { echo "Build correcto: ${env.APP_VERSION}" }
    }
}
