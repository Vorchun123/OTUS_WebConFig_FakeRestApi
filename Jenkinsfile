pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                bat '''
                    C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                    pip install pytest pytest-cov allure-pytest flake8
                '''
            }
        }
        stage('API Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest -m api --alluredir=allure-results
                '''
            }
        }
        stage('UI Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest -m ui --headless --alluredir=allure-results
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Проверка качества кода...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    if exist flake8.log del flake8.log
                    flake8 backend frontend --max-line-length=100 --format=pylint > flake8.log || exit 0
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   results: [[path: 'allure-results']]
            recordIssues(
                tools: [flake8(pattern: 'flake8.log')]
            )
        }
        success {
            echo '✅ Сборка успешна!'
        }
        failure {
            echo '❌ Сборка провалена!'
        }
    }
}