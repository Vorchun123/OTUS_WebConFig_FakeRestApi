pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install pytest pytest-cov allure-pytest flake8
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ \
                        --alluredir=allure-result
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Проверка качества кода...'
                sh '''
                    . venv/bin/activate
                    flake8 src/ tests/ --max-line-length=100 || true
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
