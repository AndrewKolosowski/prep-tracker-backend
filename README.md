## Prerequisites

1. Select your Google Cloud project
  ```bash
  gcloud projects list
  gcloud config set project <PROJECT_NAME>
  ```

2. Enable required APIs
  ```bash
  gcloud services enable run.googleapis.com firestore.googleapis.com cloudbuild.googleapis.com
  ```
3. Initialize Firestore
  ```bash
  gcloud firestore databases create --region=us-central
  ```

## Deploy API

1. Deploy Cloud Run Function (run from root of directory)
  ```bash
  gcloud run deploy prep-tracker-api \
    --source . \
    --region us-central1 \
    --no-allow-unauthenticated
  ```
  > Note: `--no-allow-unauthenticated` keeps the service off the public internet. Only principals you grant `roles/run.invoker` can call it. (The deployer can also call it.)

(Optional) Set IAM roles for other users or service accounts
  ```bash
  gcloud run services add-iam-policy-binding prep-tracker-api \
    --region us-central1 \
    --member="user:someone@example.com" \
    --role="roles/run.invoker"
  ```

## Testing

1. Retrieve the service URL either from the Cloud Console or via the CLI:
  ```bash
  gcloud run services describe prep-tracker-api \
    --region us-central1 \
    --format="value(status.url)"
  ```

2. Replace `<URL>` with the service url
  ```bash
  curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    <URL>/health
  ```

