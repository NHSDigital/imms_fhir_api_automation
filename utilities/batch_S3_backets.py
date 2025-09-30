import boto3
from botocore.exceptions import NoCredentialsError

#    destination_bucket_name = f'immunisation-batch-{context.S3_env}-data-destinations'

def upload_file_to_s3(context):
    s3 = boto3.client('s3')

    source_bucket_name = f'immunisation-batch-{context.S3_env}-data-sources'

    try:
        s3.upload_file(local_file_path, bucket_name,)
        print("✅ Upload successful!")
    except FileNotFoundError:
        print("❌ The file was not found.")
    except NoCredentialsError:
        print("❌ AWS credentials not available.")
    except Exception as e:
        print(f"❌ Upload failed: {e}")