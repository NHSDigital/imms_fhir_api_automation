import os
import pytest
import allure
from pytest_bdd import given, when, then
from utilities.genToken import get_access_token, is_token_valid
from utilities.awsToken import *
from utilities.helper import deleteCreate
from utilities.context import ScenarioContext
from dotenv import load_dotenv

access_token_global = None
expires_in_global = None
current_time_global = None
scenario_counter = 0

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    for item in items:
        if "Scenario" in item.nodeid:
            item.nodeid = item.nodeid.replace("_", " ")

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    if not step.failed: 
        message = f"✅ Step Passed: **{step.name}"
        allure.attach(message, name=f"Step Passed: {step.name}", attachment_type=allure.attachment_type.TEXT)

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_step_error(request, feature, scenario, step, exception):
    message = f"❌ Step failed! **{step.name}** \n Error: {exception}"
    allure.attach(message, name=f"Step Failed: {step.name}", attachment_type=allure.attachment_type.TEXT)

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    allure.dynamic.epic("Immunization Service")
    allure.dynamic.suite(feature.name)  # Separates features into distinct suites
    allure.dynamic.feature(feature.name)  # Ensures correct feature grouping
    allure.dynamic.title(scenario.name)

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    deleteCreate("output/allure-results")
    deleteCreate("output/allure-report")
    load_dotenv()

@pytest.fixture
def context(request) -> ScenarioContext:
    global access_token_global, expires_in_global, current_time_global, scenario_counter
    
    ctx = ScenarioContext()
    
    env_vars = [
        "auth_client_Secret", "auth_client_Id", "auth_url", "token_url",
        "callback_url", "baseUrl", "username", "scope"
    ]

    for var in env_vars:
        setattr(ctx, var, os.getenv(var))

    node = request.node
    tags = [marker.name for marker in node.own_markers] 
   
    if any(tag in tags for tag in ["Search_Feature", "Create_Feature"]):
        if scenario_counter == 0:
            access_token_global = expires_in_global = current_time_global = None

        if not is_token_valid(expires_in_global, current_time_global):
            access_token_global, expires_in_global, current_time_global = get_access_token(ctx)

        ctx.token = access_token_global
        ctx.token_expires_in = expires_in_global
        ctx.token_gen_time = current_time_global
        scenario_counter += 1

    if "Create_Feature" in tags:
        set_aws_session_token()

    for tag in tags:
        if tag.startswith('vaccine_type_'):
            ctx.vaccine_type = tag.split('vaccine_type_')[1]
        if tag.startswith('patient_id_'):
            ctx.patient_id = tag.split('patient_id_')[1]

    return ctx
