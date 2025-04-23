from utilities.helper import *
import json
import os
import uuid
from utilities.config import *
from boto3.dynamodb.conditions import Key, Attr
from delta.deltaHelper import *

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

config = getConfigParser()

import boto3
from configparser import ConfigParser

config = ConfigParser()
config.read('utilities/properties.ini')

a = [{'NHS_NUMBER': '9452372249', 'PERSON_FORENAME': 'test2', 'PERSON_SURNAME': 'test1', 'PERSON_DOB': '19800101'}]
print(a[0]['PERSON_DOB'])