import shutil
from utilities.soft_assertions import SoftAssertions 
# from behave import before_scenario
from utilities.genToken import *
from utilities.awsToken import *
from utilities.helper import *

# import logging
# logging.basicConfig(filename='debugLog.log', level=logging.INFO)
# logger = logging.getLogger(__name__)

def before_all(context):
    # Initialize a counter to track scenario execution
    context.scenario_counter = 0

    #Delete the allure-result & allure-report folder and recreate it 
    allure_results_dir = "output/allure-results"
    allure_report_dir = "output/allure-report"
    deleteCreate(allure_results_dir)
    deleteCreate(allure_report_dir)


def before_scenario(context, scenario):
    
    context.soft_assertions = SoftAssertions()
    # feature_name = scenario.feature.name
    # scenario_name = scenario.name
    
    if "Search_Feature" in scenario.feature.tags or "Create_Feature" in scenario.feature.tags:

        # global access_token_global
        if context.scenario_counter == 0:
            access_token_global = None
            expires_in_global = None
            current_time_global = None
        
        validateToken = is_token_valid(expires_in_global, current_time_global)

        if not validateToken: 
            access_token_global, expires_in_global, current_time_global = get_access_token()
        
        context.token = access_token_global
        context.token_expires_in = expires_in_global
        context.token_gen_time = current_time_global
        context.scenario_counter += 1

    if "Create_Feature" in scenario.feature.tags:
        set_aws_session_token()