import boto3
import time
from botocore.exceptions import NoCredentialsError, ClientError

def upload_file_to_S3(context):
    s3 = boto3.client("s3")
    source_bucket = f"immunisation-batch-{context.S3_env}-data-sources"
    file_path = f"{context.working_directory}/{context.filename}"
    try:
        s3.upload_file(file_path, source_bucket, context.filename)
        print(f"Upload successful: {context.filename} → {source_bucket}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"Upload failed: {e}")

def wait_for_file_to_move_archive(context, timeout=120, interval=5):
    s3 = boto3.client("s3")
    source_bucket = f"immunisation-batch-{context.S3_env}-data-sources"
    archive_key = f"archive/{context.filename}"
    file_path = f"{context.working_directory}/{context.filename}"
    print(f"Waiting for file in archive: s3://{source_bucket}/{archive_key}")
    elapsed = 0

    while elapsed < timeout:
        try:
            s3.head_object(Bucket=source_bucket, Key=archive_key)
            print(f"File found in archive: {archive_key}")
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"Still waiting... ({elapsed}s)")
            else:
                print(f"Unexpected error: {e}")
                return False
        time.sleep(interval)
        elapsed += interval

    print(f"Timeout: File not found in archive after {timeout} seconds")
    return False

def wait_and_read_ack_file(context, folderName: str, timeout=120, interval=5):
    s3 = boto3.client("s3")
    destination_bucket = f"immunisation-batch-{context.S3_env}-data-destinations"
    source_filename = context.filename
    base_name = source_filename.replace(f'.{context.file_extension}', "")
    forwarded_prefix = f"{folderName}/{base_name}"
    
    context.forwarded_prefix = forwarded_prefix

    print(f"Waiting for file starting with '{forwarded_prefix}' in bucket: {destination_bucket}")
    elapsed = 0

    while elapsed < timeout:
        try:
            response = s3.list_objects_v2(Bucket=destination_bucket, Prefix=forwarded_prefix)
            contents = response.get("Contents", [])
            if contents:
                key = contents[0]["Key"]
                print(f"File found: {key}")

                # Read file contents
                obj = s3.get_object(Bucket=destination_bucket, Key=key)
                file_data = obj["Body"].read().decode("utf-8")
                print(f"File contents loaded ({len(file_data)} bytes)")
                return file_data

            else:
                print(f"Still waiting... ({elapsed}s)")
        except ClientError as e:
            print(f"Error checking bucket: {e}")
            return None

        time.sleep(interval)
        elapsed += interval

    print(f"Timeout: No file found with prefix '{forwarded_prefix}' after {timeout} seconds")
    return None
