pipeline{
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "direct-byte-450314-k1"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        AR_LOCATION = "us-central1"
        AR_REPO = "ml-project-repo"
    }
    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/sarazayan/MLOPS-Course-Project1']])
                }
            }
        }
        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building and Pushing Docker Image to Artifact Registry'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to Artifact Registry.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker ${AR_LOCATION}-docker.pkg.dev --quiet
                        docker build -t ${AR_LOCATION}-docker.pkg.dev/${GCP_PROJECT}/${AR_REPO}/ml-project:latest .
                        docker push ${AR_LOCATION}-docker.pkg.dev/${GCP_PROJECT}/${AR_REPO}/ml-project:latest 
                        '''
                    }
                }
            }
        }
        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud run deploy ml-project \
                            --image=${AR_LOCATION}-docker.pkg.dev/${GCP_PROJECT}/${AR_REPO}/ml-project:latest \
                            --platform=managed \
                            --region=${AR_LOCATION} \
                            --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
}