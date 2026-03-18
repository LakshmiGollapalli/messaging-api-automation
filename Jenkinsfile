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
                 echo 'Stopping existing app (if running)...'
                 bat 'taskkill /F /IM python.exe || exit 0'
                 echo 'Deploying application...'
                 dir('messaging-api-automation') {
                     bat 'python app.py'
                 }

            }
        }
  }
  }
