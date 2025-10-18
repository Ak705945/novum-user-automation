import allure
from typing import Any, Dict
from common.logger import logger


class Assertions:
    """Custom assertion methods with detailed error messages"""

    @staticmethod
    def assert_status_code(actual: int, expected: int, message: str = ""):
        """Assert HTTP status code"""
        try:
            assert actual == expected, \
                f"Status code mismatch. Expected: {expected}, Actual: {actual}. {message}"
            logger.info(f"✓ Status code assertion passed: {actual}")
        except AssertionError as e:
            logger.error(f"✗ Status code assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise

    @staticmethod
    def assert_response_code(response: Dict, expected: int = 200, message: str = ""):
        """Assert response code in JSON body"""
        actual = response.get('code')
        try:
            assert actual == expected, \
                f"Response code mismatch. Expected: {expected}, Actual: {actual}. {message}"
            logger.info(f"✓ Response code assertion passed: {actual}")
        except AssertionError as e:
            logger.error(f"✗ Response code assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise

    @staticmethod
    def assert_response_message(response: Dict, expected: str, message: str = ""):
        """Assert response message"""
        actual = response.get('msg')
        try:
            assert actual == expected, \
                f"Response message mismatch. Expected: '{expected}', Actual: '{actual}'. {message}"
            logger.info(f"✓ Response message assertion passed: {actual}")
        except AssertionError as e:
            logger.error(f"✗ Response message assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise

    @staticmethod
    def assert_field_exists(response: Dict, field: str, message: str = ""):
        """Assert field exists in response"""
        try:
            assert field in response, \
                f"Field '{field}' not found in response. {message}"
            logger.info(f"✓ Field existence assertion passed: {field}")
        except AssertionError as e:
            logger.error(f"✗ Field existence assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise

    @staticmethod
    def assert_field_value(response: Dict, field: str, expected: Any, message: str = ""):
        """Assert field value in response"""
        actual = response.get(field)
        try:
            assert actual == expected, \
                f"Field '{field}' value mismatch. Expected: {expected}, Actual: {actual}. {message}"
            logger.info(f"✓ Field value assertion passed: {field}={actual}")
        except AssertionError as e:
            logger.error(f"✗ Field value assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise

    @staticmethod
    def assert_not_none(value: Any, field_name: str = "Value", message: str = ""):
        """Assert value is not None"""
        try:
            assert value is not None, \
                f"{field_name} should not be None. {message}"
            logger.info(f"✓ Not None assertion passed: {field_name}")
        except AssertionError as e:
            logger.error(f"✗ Not None assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise

    @staticmethod
    def assert_list_not_empty(value: list, field_name: str = "List", message: str = ""):
        """Assert list is not empty"""
        try:
            assert isinstance(value, list) and len(value) > 0, \
                f"{field_name} should be a non-empty list. {message}"
            logger.info(f"✓ List not empty assertion passed: {field_name} (length: {len(value)})")
        except AssertionError as e:
            logger.error(f"✗ List not empty assertion failed: {str(e)}")
            allure.attach(str(e), "Assertion Error", allure.attachment_type.TEXT)
            raise


# Singleton instance
assertions = Assertions()