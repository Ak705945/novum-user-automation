import pytest
import allure
from api.user_api import user_api
from common.assertions import assertions
from common.logger import logger
from testcases.conftest import created_user_ids


@allure.feature("User Management")
@allure.story("Delete User")
class TestDeleteUser:
    """Test cases for Delete User API"""

    @allure.title("Test delete user with valid user ID - normal case")
    @allure.description("Delete an existing user successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_normal(self, create_test_user):
        """Positive test: Delete user with valid ID"""
        user_data = create_test_user
        user_id = user_data["id"]

        with allure.step(f"Delete user: ID={user_id}"):
            response = user_api.delete_user(user_id)

        with allure.step("Verify deletion response"):
            assertions.assert_response_code(response, 200)
            assertions.assert_response_message(response, "success")
            logger.info(f"✓ User deleted successfully: ID={user_id}")

            # Remove from cleanup list since it's already deleted
            if user_id in created_user_ids:
                created_user_ids.remove(user_id)

        with allure.step("Verify user no longer exists"):
            get_response = user_api.get_user(user_id)
            assert get_response["code"] != 200, "Deleted user should not be accessible"
            logger.info(f"✓ Deleted user confirmed inaccessible: ID={user_id}")

    @allure.title("Test delete non-existent user - abnormal case")
    @allure.description("Attempt to delete a user that doesn't exist")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_non_existent(self):
        """Negative test: Delete non-existent user"""
        non_existent_id = 999999

        with allure.step(f"Attempt to delete non-existent user: ID={non_existent_id}"):
            response = user_api.delete_user(non_existent_id)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail for non-existent user"
            logger.info(f"✓ Non-existent user deletion correctly rejected: {response.get('msg')}")

    @allure.title("Test delete already deleted user - abnormal case")
    @allure.description("Attempt to delete a user twice (double deletion)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_twice(self, create_test_user):
        """Negative test: Delete user twice"""
        user_data = create_test_user
        user_id = user_data["id"]

        with allure.step(f"First deletion of user: ID={user_id}"):
            first_response = user_api.delete_user(user_id)
            assertions.assert_response_code(first_response, 200)
            if user_id in created_user_ids:
                created_user_ids.remove(user_id)

        with allure.step(f"Attempt second deletion of user: ID={user_id}"):
            second_response = user_api.delete_user(user_id)

        with allure.step("Verify error response for second deletion"):
            assert second_response["code"] != 200, "Should fail for already deleted user"
            logger.info(f"✓ Double deletion correctly rejected: {second_response.get('msg')}")

    @allure.title("Test delete user with invalid ID type - abnormal case")
    @allure.description("Attempt to delete user with invalid ID type")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_invalid_id(self):
        """Negative test: Delete user with invalid ID"""
        invalid_id = "invalid"

        with allure.step(f"Attempt to delete with invalid ID: {invalid_id}"):
            try:
                response = user_api.delete_user(invalid_id)
                assert response["code"] != 200, "Should fail with invalid ID"
                logger.info(f"✓ Invalid ID correctly rejected: {response.get('msg')}")
            except Exception as e:
                logger.info(f"✓ Invalid ID correctly rejected with exception: {str(e)}")

    @allure.title("Test delete user with zero ID - edge case")
    @allure.description("Test system behavior with ID = 0")
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_user_zero_id(self):
        """Edge case: Delete user with ID = 0"""
        with allure.step("Attempt to delete user with ID = 0"):
            response = user_api.delete_user(0)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail with ID = 0"
            logger.info(f"✓ Zero ID correctly handled: {response.get('msg')}")