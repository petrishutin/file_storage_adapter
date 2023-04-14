# File Storage Adapter

This is a simple file storage adapter for different services:

- [Local] (Uses the local filesystem)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Google Cloud Storage](https://cloud.google.com/storage/)

## Principal features

- Takes bytes and return UUID at '<host>/'
- Take UUID and return bytes in file exists at '<host>/{uuid}'
- Delete file by UUID '<host>/{uuid}'

You can find the API documentation at '<host>/docs' in TEST_MODE

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

- AWS_REGION_NAME
- AWS_ENDPOINT_URL
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

You can find examples of these variables in the app/settings.py file.
