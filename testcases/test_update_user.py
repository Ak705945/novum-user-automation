import pytest
import allure
from faker import Faker
from api.user_api import user_api
from common.assertions import assertions
from common.config_reader import config_reader
from common.logger import logger



@allure.feature("User Management")
@allure.story("Update User Email")
class TestUpdateUser:
    """Test cases for Update User Email API"""

    @allure.title("Test update user email with valid data - normal case")
    @allure.description("Update user's email with a valid new email address")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_email_normal(self, create_test_user):
        """Positive test: Update user email with valid data"""
        user_data = create_test_user
        user_id = user_data["id"]
        new_email = config_reader.get_test_data("newEmail")

        with allure.step(f"Update user {user_id} email to: {new_email}"):
            response = user_api.update_user_email(user_id, new_email)

        with allure.step("Verify update response"):
            assertions.assert_response_code(response, 200)
            assertions.assert_response_message(response, "success")
            logger.info(f"✓ User email updated successfully: ID={user_id}")

        with allure.step("Verify email was updated by getting user details"):
            get_response = user_api.get_user(user_id)
            assertions.assert_response_code(get_response, 200)
            assertions.assert_field_value(get_response["data"], "email", new_email)
            logger.info(f"✓ Email update verified: {new_email}")

    @allure.title("Test update user email for non-existent user - abnormal case")
    @allure.description("Attempt to update email for a non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_email_non_existent(self):
        """Negative test: Update email for non-existent user"""
        non_existent_id = 999999
        new_email = config_reader.get_test_data("newEmail")

        with allure.step(f"Attempt to update non-existent user {non_existent_id}"):
            response = user_api.update_user_email(non_existent_id, new_email)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail for non-existent user"
            logger.info(f"✓ Non-existent user update correctly rejected: {response.get('msg')}")

    @allure.title("Test update user email with invalid format - abnormal case")
    @allure.description("Attempt to update user's email with invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_email_invalid_format(self, create_test_user):
        """Negative test: Update email with invalid format"""
        user_data = create_test_user
        user_id = user_data["id"]
        invalid_emails = config_reader.get_test_data("invalid_emails")

        for invalid_email in invalid_emails[:2]:
            with allure.step(f"Attempt to update with invalid email: {invalid_email}"):
                response = user_api.update_user_email(
                    user_id,
                    invalid_email,
                    validate=False
                )

            with allure.step("Verify error response"):
                assert response["code"] != 200, f"Should fail with invalid email: {invalid_email}"
                logger.info(f"✓ Invalid email format correctly rejected: {invalid_email}")

    @allure.title("Test update email for deleted user - abnormal case")
    @allure.description("Attempt to update email for a user that has been deleted")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_deleted_user_email(self, create_test_user):
        """Negative test: Update email for deleted user"""
        user_data = create_test_user
        user_id = user_data["id"]
        new_email = config_reader.get_test_data("newEmail")

        with allure.step(f"Delete user: ID={user_id}"):
            delete_response = user_api.delete_user(user_id)
            assertions.assert_response_code(delete_response, 200)

        with allure.step(f"Attempt to update deleted user's email"):
            response = user_api.update_user_email(user_id, new_email)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail for deleted user"
            logger.info(f"✓ Deleted user update correctly rejected: {response.get('msg')}")

    @allure.title("Test update user email with empty string - edge case")
    @allure.description("Test system behavior with empty email string")
    @allure.severity(allure.severity_level.MINOR)
    def test_update_user_email_empty(self, create_test_user):
        """Edge case: Update email with empty string"""
        user_data = create_test_user
        user_id = user_data["id"]

        with allure.step("Attempt to update with empty email"):
            response = user_api.update_user_email(user_id, "", validate=False)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail with empty email"
            logger.info(f"✓ Empty email correctly rejected: {response.get('msg')}")

    @allure.title("Test update user email with very long email - edge case")
    @allure.description("Test system behavior with extremely long email address")
    @allure.severity(allure.severity_level.MINOR)
    def test_update_user_email_very_long(self, create_test_user):
        """Edge case: Update email with very long email address"""
        user_data = create_test_user
        user_id = user_data["id"]
        long_email = "a" * 200 + "@example.com"

        with allure.step(f"Attempt to update with {len(long_email)}-character email"):
            response = user_api.update_user_email(user_id, long_email, validate=False)

        with allure.step("Verify response"):
            if response["code"] == 200:
                logger.info("✓ Very long email accepted")
            else:
                logger.info(f"✓ Very long email rejected: {response.get('msg')}")
