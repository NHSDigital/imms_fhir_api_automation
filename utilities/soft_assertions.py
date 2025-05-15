import allure
from allure_commons.types import AttachmentType



class SoftAssertions():
    def __init__(self):
        # self.driver = driver
        self.failures = []

    # def capture_screenshot_on_failure(driver):
    #     screenshot_path = "screenshot_failure.png"
    #     driver.save_screenshot(screenshot_path)

    #     with open(screenshot_path, "rb") as screenshot_file:
    #         allure.attach(screenshot_file.read(), name="Failure Screenshot", attachment_type=AttachmentType.PNG)
            

    def assert_condition(self, condition, message="Assertion failed"):
       with allure.step(message):
            if not condition:
                self.failures.append(message)
                allure.attach(
                    body=f"Failed condition: {message}",
                    name="Soft Assertion Failure",
                    attachment_type=allure.attachment_type.TEXT
                )
                # self.capture_screenshot_on_failure(self.driver)
                # raise AssertionError(message) 

                # allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)


    def assert_all(self):
        if self.failures:
            failure_message = "\n".join(self.failures)
            self.failures.clear()
            allure.attach(
                body=f"Summary of Soft Assertion Failures:\n{failure_message}",
                name="Soft Assertions Summary",
                attachment_type=allure.attachment_type.TEXT
            )
            raise AssertionError("One or more soft assertions failed")


