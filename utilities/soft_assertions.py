import allure

class SoftAssertions:
    def __init__(self):
        self.failures = []

    def assert_condition(self, condition, message="Assertion failed"):
        with allure.step(message):
            if not condition:
                self.failures.append(message)
                allure.attach(
                    body=f"Failed condition: {message}",
                    name="Soft Assertion Failure",
                    attachment_type=allure.attachment_type.TEXT
                )

    def assert_all(self):
        if self.failures:
            failure_message = "\n".join(self.failures)
            allure.attach(
                body=f"Summary of Soft Assertion Failures:\n{failure_message}",
                name="Soft Assertions Summary",
                attachment_type=allure.attachment_type.TEXT
            )
            raise AssertionError("One or more soft assertions failed")

