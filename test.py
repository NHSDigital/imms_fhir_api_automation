from utilities.helper import *
import json
import os
import uuid
from utilities.config import *
import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

config = getConfigParser()

import boto3
from configparser import ConfigParser

config = ConfigParser()
config.read('utilities/properties.ini')


def switch_case(option):
    switch = {
        840539006: "COVID19",
        6142004: "FLU",
        55735004: "RSV",
    }
    return switch.get(option, "Invalid option")

option = int("55735004")
print(switch_case(option))    