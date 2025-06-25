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

def deleteCreate(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def format_timestamp(timestamp):
    parts = timestamp.split(".")

    if len(parts) == 2:
        milliseconds, timezone = parts[1].split("+")
        milliseconds = milliseconds.ljust(6, "0")
        
        return f"{parts[0]}.{milliseconds}+{timezone}"


def readInputCSV_search():
    with open('input_csv_files/searchParams.csv') as searchCSV:
        searchReader = csv.reader(searchCSV,delimiter=',')

        for row in searchReader:
            print(row)

def covert_to_expected_date_format(date_string):
    try:
        return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    except ValueError:
        return "Invalid format"
    
def iso_to_compact(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.strftime("%Y%m%dT%H%M%S00")
