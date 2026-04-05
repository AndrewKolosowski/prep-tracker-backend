## Deploying API Instructions

1. Set your Google Cloud project using: `gcloud config set project <PROJECT_NAME>`

2. From this directory deploy the Cloud Run Function
```bash
gcloud run deploy prep-tracker-api \
  --source . \
  --region us-central1 \
  --no-allow-unauthenticated
```

`--no-allow-unauthenticated` keeps the service off the public internet; only principals you grant `roles/run.invoker` can call it. (Also the deployer can access it)

### Test calling the API yourself

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