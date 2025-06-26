import csv
from datetime import datetime
import os
import shutil
from utilities.soft_assertions import SoftAssertions
from utilities.config import *


soft_assertions = SoftAssertions()
config = getConfigParser()

import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def empty_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def covert_to_expected_date_format(date_string):
    try:
        return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    except ValueError:
        return "Invalid format"
    
def iso_to_compact(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.strftime("%Y%m%dT%H%M%S00")

gender_map = {
    "male": "1",
    "female": "2",
    "unknown": "0",
    "other": "9"
}
