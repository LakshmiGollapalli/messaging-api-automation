pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                bat 'flake8 .'
            }
        }

        stage('Test') {
            steps {
                bat 'pytest -v'
            }
        }

        stage('Deploy') {
            steps {
                 echo 'Deploying application...'
                 dir('messaging-api-automation') {
                     bat 'start /B python app.py'
                     }
            }
        }
    }
}