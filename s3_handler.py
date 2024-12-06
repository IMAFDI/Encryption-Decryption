import boto3
from botocore.exceptions import NoCredentialsError
import os

from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET

def upload_to_s3(file_path, s3_key):
    try:
        # Initialize the S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        # Upload the file
        s3.upload_file(file_path, S3_BUCKET, s3_key)


        # Generate a presigned URL for download (valid for 24 hours)
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_key},
            ExpiresIn=86400  # 24 hours
        )

        # Delete the local file after upload
        os.remove(file_path)

        return True, f"Uploaded to S3 as {s3_key}", presigned_url
    except FileNotFoundError:
        return False, "File not found!", None
    except NoCredentialsError:
        return False, "AWS credentials not found!", None
    except Exception as e:
        return False, str(e), None