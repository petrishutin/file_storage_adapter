# File Storage Adapter

This is a simple file storage adapter for different services:

- [Local] (Uses the local filesystem)
- [Amazon S3 or compatible](https://aws.amazon.com/s3/)
- [Google Cloud Storage](https://cloud.google.com/storage/)

## Principal features

- Takes bytes and return UUID at '{host}/'
- Take UUID and return bytes in file exists at '{host}/{uuid}'
- Delete file by UUID '{host}/{uuid}'

You can find the API documentation at '{host}/docs'

## Installation

```bash
pip install -r requirements.txt
```

## Running with local storage

```bash
uvicorn main:app --reload
```

## Running with Amazon S3

Same as above, but with the following environment variables:

- FILE_STORAGE_TYPE=S3FileStorage
- BUCKETS=<names of existing buckets separated by comma>
- AWS_REGION_NAME=<your region here>
- AWS_ENDPOINT_URL=<your provider storage url here>
- AWS_ACCESS_KEY_ID=<your access key here>
- AWS_SECRET_ACCESS_KEY=<your secret key here>

You can find examples of these variables in the app/settings.py file.

## Running with Google Cloud Storage

Same as above, but with the following environment variables:

- FILE_STORAGE_TYPE=GoogleCloudStorage
- BUCKETS=<names of existing buckets separated by comma>
- GOOGLE_APPLICATION_CREDENTIALS=<path to your credentials file>

You can find examples of these variables in the app/settings.py file.