pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR', defaultValue: 'selenoid', description: 'Selenoid hub host')
        string(name: 'APP_URL', defaultValue: 'http://prestashop', description: 'PrestaShop application URL')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser to run tests in')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0', description: 'Browser version on Selenoid (Chrome 128.0/127.0, Firefox 125.0/124.0)')
        string(name: 'THREADS', defaultValue: '2', description: 'Number of parallel test threads')
    }

    stages {
        stage('Run tests') {
            steps {
                sh "pytest --url ${params.APP_URL} --executor ${params.EXECUTOR} --browser ${params.BROWSER} --browser_version ${params.BROWSER_VERSION} -n ${params.THREADS} --alluredir=allure-results -v"
            }
        }
    }

    post {
        always {
            allure(results: [[path: 'allure-results']])
        }
    }
}
