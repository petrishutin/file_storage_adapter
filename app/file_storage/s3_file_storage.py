from uuid import uuid4

from aiobotocore.session import get_session  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from app.file_storage.base_file_storage import FileStorage


class S3FileStorage(FileStorage):
    def __init__(self, service_settings):
        super().__init__(service_settings)
        self.aws_access_key_id = service_settings.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = service_settings.AWS_SECRET_ACCESS_KEY
        self.region_name = service_settings.AWS_REGION_NAME
        self.endpoint_url = service_settings.AWS_ENDPOINT_URL
        self.session = get_session()
        self.bucket_list = service_settings.BUCKET_LIST

    def _create_client(self):
        return self.session.create_client(
            "s3",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url,
        )

    async def _init_buckets(self):
        """Function to set up bucket in S3 in test mode.
        This method for test mode only. In production init your buckets outside the application"""
        async with self._create_client() as client:
            buckets_at_remote = await client.list_buckets()
            for bucket in self.bucket_list:
                if bucket not in buckets_at_remote["Buckets"]:
                    await client.create_bucket(Bucket=bucket)

    async def upload(self, file_data: bytes) -> str:
        filename = str(uuid4())
        bucket = self._get_bucket_name(str(filename))
        async with self._create_client() as client:
            self._check_bucket(bucket)
            await client.put_object(Bucket=bucket, Key=filename, Body=file_data)
            return filename

    async def download(self, filename: str) -> bytes:
        bucket = self._get_bucket_name(str(filename))
        async with self._create_client() as client:
            self._check_bucket(bucket)
            try:
                response = await client.get_object(Bucket=bucket, Key=filename)
            except ClientError as e:
                raise FileNotFoundError(f"File not found: {e}")
            return await response["Body"].read()

    async def delete(self, filename: str) -> None:
        bucket = self._get_bucket_name(str(filename))
        async with self._create_client() as client:
            self._check_bucket(bucket)
            try:
                await client.get_object(Bucket=bucket, Key=filename)
            except ClientError as e:
                raise FileNotFoundError(f"File not found {e}")
            await client.delete_object(Bucket=bucket, Key=filename)
            return None
