// Jenkinsfile Pipeline CI/CD SentimentAI
pipeline {
    agent any

    environment {
        // Nom de l'image Docker
        IMAGE_NAME = 'sentiment-ai'
        // Registry GitHub (remplacez VOTRE_PSEUDO)
        REGISTRY = 'ghcr.io/MaximeBuchet'.toLowerCase()
        // Tag = 7 premiers caractères du SHA Git
        IMAGE_TAG = sh(script: 'git rev-parse --short HEAD', returnStdout:true).trim()
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Jenkins clone automatiquement le repo configuré dans le job
                checkout scm
                echo "Branche : ${env.BRANCH_NAME}"
                echo "Commit : ${env.GIT_COMMIT}"
                sh 'git log --oneline -5'
            }
        }

        stage('Lint') {
            steps {
                // Lancer flake8 dans un conteneur Python temporaire
                // --rm supprime le conteneur après l'exécution
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        python:3.11-slim \
                        sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"
                '''
            }
        }

        stage('Build & Test') {
            steps {
                // Construire l'image Docker
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."

                // Lancer pytest dans le conteneur fraichement construit
                sh '''
                    docker run --rm \
                        -e CI=true \
                        ''' + "${IMAGE_NAME}:${IMAGE_TAG}" + ''' \
                        pytest tests/ -v \
                            --cov=src \
                            --cov-report=term-missing \
                            --cov-fail-under=70
                '''
            }
            post {
                failure {
                    echo 'Tests echoues ou coverage insuffisant (< 70%)'
                }
            }
        }

        stage('Push') {
            // Ce stage ne s'exécute QUE sur la branche main
            when {
                //branch 'main'
                expression { env.GIT_BRANCH?.endsWith('/main') }
            }
            steps {
                // Se connecter au registry avec les credentials Jenkins
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
                    sh '''
                        # Login au registry
                        echo $REGISTRY_PASS | docker login ghcr.io \
                            -u $REGISTRY_USER --password-stdin

                        # Tagger avec le SHA Git
                        docker tag ''' + "${IMAGE_NAME}:${IMAGE_TAG}" + ''' \
                            ''' + "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}" + '''

                        # Tagger aussi comme 'latest' de la branche main
                        docker tag ''' + "${IMAGE_NAME}:${IMAGE_TAG}" + ''' \
                            ''' + "${REGISTRY}/${IMAGE_NAME}:main" + '''

                        # Pousser les deux tags
                        docker push ''' + "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}" + '''
                        docker push ''' + "${REGISTRY}/${IMAGE_NAME}:main" + '''
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline reussi ! Image : ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline echoue. Consultez les logs ci-dessus.'
        }
        always {
            // Nettoyer les conteneurs de test
            sh 'docker compose down -v 2>/dev/null || true'
        }
    }
}