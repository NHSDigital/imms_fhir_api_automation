import json
import os
import boto3
import botocore

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def set_aws_session_token():
    try:
        print("token started.......")
        # Create a session using your AWS credentials
        session = boto3.Session()

        # Get the credentials object
        credentials = session.get_credentials()
        
        # Refresh credentials if needed and retrieve the session token
        credentials = credentials.get_frozen_credentials()
        access_key = credentials.access_key
        secret_key = credentials.secret_key
        session_token = credentials.token

        # Use os.system to call AWS CLI commands and set credentials
        os.system(f"aws configure set aws_access_key_id {access_key}")
        os.system(f"aws configure set aws_secret_access_key {secret_key}")
        os.system(f"aws configure set aws_session_token {session_token}")

    except Exception as e:
        print(f"Error setting AWS session token: {e}")
