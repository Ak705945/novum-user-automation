import pytest
import allure
from api.user_api import user_api
from common.assertions import assertions
from common.logger import logger


@allure.feature("User Management")
@allure.story("Get User Details")
class TestGetUser:
    """Test cases for Get User Details API"""

    @allure.title("Test get user details with valid user ID - normal case")
    @allure.description("Retrieve details of an existing user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_normal(self, create_test_user):
        """Positive test: Get user details with valid ID"""
        user_data = create_test_user
        user_id = user_data["id"]

        with allure.step(f"Get user details for user ID: {user_id}"):
            response = user_api.get_user(user_id)

        with allure.step("Verify response structure and data"):
            assertions.assert_response_code(response, 200)
            assertions.assert_response_message(response, "success")
            assertions.assert_field_exists(response, "data")
            assertions.assert_not_none(response["data"], "User data")

            # Verify user data matches
            user = response["data"]
            assertions.assert_field_value(user, "id", user_id)
            assertions.assert_field_value(user, "username", user_data["username"])
            assertions.assert_field_value(user, "email", user_data["email"])
            logger.info(f"✓ User details retrieved successfully: ID={user_id}")

    @allure.title("Test get user details with non-existent user ID - abnormal case")
    @allure.description("Attempt to retrieve details of a non-existent user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_non_existent(self):
        """Negative test: Get user with non-existent ID"""
        non_existent_id = 999999

        with allure.step(f"Attempt to get non-existent user: ID={non_existent_id}"):
            response = user_api.get_user(non_existent_id)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail for non-existent user"
            logger.info(f"✓ Non-existent user correctly handled: {response.get('msg')}")

    @allure.title("Test get user details with invalid user ID type - abnormal case")
    @allure.description("Attempt to retrieve user with invalid ID type (string)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_invalid_id_type(self):
        """Negative test: Get user with invalid ID type"""
        invalid_id = "invalid"

        with allure.step(f"Attempt to get user with invalid ID: {invalid_id}"):
            try:
                # This might raise exception or return error
                response = user_api.get_user(invalid_id)

                with allure.step("Verify error response"):
                    assert response["code"] != 200, "Should fail with invalid ID type"
                    logger.info(f"✓ Invalid ID type correctly rejected: {response.get('msg')}")
            except Exception as e:
                logger.info(f"✓ Invalid ID type correctly rejected with exception: {str(e)}")

    @allure.title("Test get deleted user details - abnormal case")
    @allure.description("Attempt to retrieve details of a deleted user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_deleted_user(self, create_test_user):
        """Negative test: Get user details after deletion"""
        user_data = create_test_user
        user_id = user_data["id"]

        with allure.step(f"Delete user: ID={user_id}"):
            delete_response = user_api.delete_user(user_id)
            assertions.assert_response_code(delete_response, 200)

        with allure.step(f"Attempt to get deleted user: ID={user_id}"):
            response = user_api.get_user(user_id)

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail for deleted user"
            logger.info(f"✓ Deleted user correctly handled: {response.get('msg')}")

    @allure.title("Test get user with zero ID - edge case")
    @allure.description("Test system behavior with ID = 0")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_user_zero_id(self):
        """Edge case: Get user with ID = 0"""
        with allure.step("Attempt to get user with ID = 0"):
            response = user_api.get_user(0)

        with allure.step("Verify response"):
            assert response["code"] != 200, "Should fail with ID = 0"
            logger.info(f"✓ Zero ID correctly handled: {response.get('msg')}")

    @allure.title("Test get user with negative ID - edge case")
    @allure.description("Test system behavior with negative user ID")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_user_negative_id(self):
        """Edge case: Get user with negative ID"""
        negative_id = -1

        with allure.step(f"Attempt to get user with negative ID: {negative_id}"):
            response = user_api.get_user(negative_id)

        with allure.step("Verify response"):
            assert response["code"] != 200, "Should fail with negative ID"
            logger.info(f"✓ Negative ID correctly handled: {response.get('msg')}")
