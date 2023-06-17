pipeline {
    agent any

    stages {
        stage('Checkout_main') {
            steps {
                script {
                    // Get some code from a GitHub repository
                    echo 'Checkout1'
                    if (fileExists('main_project')){
                        powershell 'remove-item -r -force main_project'
                    }
                    powershell 'New-Item "main_project" -ItemType Directory'
                    dir('main_project') {
                        git credentialsId: 'github_private_key', url: 'git@github.com:samantim/QA_website.git'
                    }
                }
            }
        }
        stage('Checkout_secret') {
            steps {
                script {
                    // Get some code from a GitHub repository
                    echo 'Checkout2'
                    if (fileExists('secret')){
                        powershell 'remove-item -r -force secret'
                    }
                    powershell 'New-Item "secret" -ItemType Directory'
                    dir('secret') {
                        git credentialsId: 'github_private_key', url: 'git@github.com:samantim/secret.git'
                    }
                }
            }
        }
        stage('copy env file') {
            steps {
                powershell 'New-Item -path "main_project/backend" -name "attachments" -ItemType Directory'
                powershell 'New-Item -path "main_project/backend/tests" -name "attachments" -ItemType Directory'
                powershell 'copy "secret/qa_website/.env" "main_project/backend/.env"'
                powershell 'copy "secret/qa_website/.env" "main_project/backend/tests/.env"'
            }
        }
        stage('Test') {
            steps {
                // Test using pytest
                echo 'test stage'
                dir('main_project/backend/tests') {
                    powershell 'python -m pytest -v'
                }
            }
        }
        stage('Deploy') {
            steps {
                // run 
                echo 'deploy stage'
                dir('main_project/backend'){
                    powershell 'python -m uvicorn main:app'
                }
            }
        }
    }
}
