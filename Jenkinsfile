pipeline {
    agent none

    stages {
        stage('Build') {
            agent {
                docker {
                    image 'kuralabs/python3-dev:latest'
                    args '-u root:root'
                }
            }

            steps {
                sh '''
                    tox -e build
                    tox -e test
                    tox -e doc
                '''
                stash name: 'docs', includes: '.tox/env/tmp/html/**/*'
            }
        }

        stage('Publish') {
            agent { label 'docs' }
            when { branch 'master' }
            steps {
                unstash 'docs'
                sh '''
                    umask 022
                    mkdir -p /deploy/docs/mivotico/tse2sql
                    rm -rf /deploy/docs/mivotico/tse2sql/*
                    cp -R .tox/env/tmp/html/* /deploy/docs/mivotico/tse2sql/
                '''
            }
        }
    }
    post {
        success {
            slackSend (
                color: '#00FF00',
                message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
            )
        }

        failure {
            slackSend (
                color: '#FF0000',
                message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
            )
        }
    }
}
