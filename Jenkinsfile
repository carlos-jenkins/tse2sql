pipeline {
    agent { label 'docker' }

    environment {
        ADJUST_USER_UID = sh(
            returnStdout: true,
            script: 'id -u'
        ).trim()
        ADJUST_USER_GID = sh(
            returnStdout: true,
            script: 'id -g'
        ).trim()
        ADJUST_DOCKER_GID = sh(
            returnStdout: true,
            script: 'getent group docker | cut -d: -f3'
        ).trim()
    }

    stages {
        stage('Build') {
            agent {
                docker {
                    alwaysPull true
                    image 'kuralabs/python3-dev:latest'
                    args '-u root:root'
                }
            }

            steps {
                sh '''
                sudo --user=python3 --set-home tox --recreate
                '''
                stash name: 'docs', includes: '.tox/env/tmp/html/**/*'
            }
        }

        stage('Publish') {
            agent { label 'docs' }
            when {
                beforeAgent true
                branch 'master'
            }
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
