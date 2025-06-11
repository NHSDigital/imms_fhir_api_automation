import json
import os
import boto3
from aws_sso_lite import get_sso_token_by_start_url, do_sso_login
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


def get_aws_token():
    start_url = "https://d-9c67018f89.awsapps.com/start/#"
    region = "eu-west-1"
    access_token = get_sso_token()
    print("Retrieved SSO Access Token:", access_token)
    # Get SSO token
    sso_token = get_sso_token_by_start_url(start_url)

    # Create a botocore session and authenticate
    botocore_session = botocore.session.Session()
    do_sso_login(botocore_session, region, start_url)

    print("AWS SSO authentication successful!")

def get_sso_token():
    sso_cache_path = os.path.expanduser("~/.aws/sso/cache")  # AWS SSO cache location
    for filename in os.listdir(sso_cache_path):
        if filename.endswith(".json"):
            with open(os.path.join(sso_cache_path, filename), "r") as f:
                data = json.load(f)
                return data.get("accessToken")  # Extract the access token

    raise ValueError("AWS SSO access token not found. Please run 'aws sso login'.")

def get_sso_credentials():
    sso_client = boto3.client("sso", region_name="eu-west-1")

    response = sso_client.list_accounts(accessToken="your-access-token")
    account_id = response["accountList"][0]["accountId"]  # Select first account
    role_name = "AWSReservedSSO_DEV-IMMS-Devops"

    # Get temporary AWS credentials for the role
    credentials = sso_client.get_role_credentials(
        accessToken="your-access-token",
        accountId=account_id,
        roleName=role_name
    )["roleCredentials"]

    return {
        "AccessKeyId": credentials["AccessKeyId"],
        "SecretAccessKey": credentials["SecretAccessKey"],
        "SessionToken": credentials["SessionToken"]
    }
