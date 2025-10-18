import pytest
import allure
from faker import Faker
from api.user_api import user_api
from common.assertions import assertions
from common.config_reader import config_reader
from common.logger import logger
from testcases.conftest import created_user_ids



@allure.feature("User Management")
@allure.story("Create User")
class TestCreateUser:
    """Test cases for Create User API"""

    @allure.title("Test create user with valid data - normal case")
    @allure.description("Create a user with all valid parameters and verify the response")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_normal(self, generate_user_data):
        """Positive test: Create user with valid data"""
        user_data = generate_user_data

        with allure.step(f"Create user with username: {user_data['username']}"):
            response = user_api.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"]
            )

        with allure.step("Verify response structure and data"):
            assertions.assert_response_code(response, 200)
            assertions.assert_response_message(response, "success")
            assertions.assert_field_exists(response, "data")
            assertions.assert_not_none(response["data"], "User data")

            # Verify user data
            user = response["data"]
            assertions.assert_field_exists(user, "id")
            assertions.assert_field_value(user, "username", user_data["username"])

            # Track for cleanup
            created_user_ids.append(user["id"])
            logger.info(f"✓ User created successfully: ID={user['id']}")

    @allure.title("Test create user with duplicate username - abnormal case")
    @allure.description("Attempt to create a user with an already existing username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_duplicate_username(self, create_test_user, generate_user_data):
        """Negative test: Create user with duplicate username"""
        existing_user = create_test_user
        new_user_data = generate_user_data

        with allure.step(f"Attempt to create user with duplicate username: {existing_user['username']}"):
            response = user_api.create_user(
                username=existing_user["username"],  # Duplicate username
                email=new_user_data["email"],  # Different email
                password=new_user_data["password"]
            )

        with allure.step("Verify error response"):
            # Expecting error code (not 200)
            assert response["code"] != 200, "Should fail with duplicate username"
            logger.info(f"✓ Duplicate username correctly rejected: {response.get('msg')}")

    @allure.title("Test create user with missing username - abnormal case")
    @allure.description("Attempt to create a user without providing username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_missing_username(self, generate_user_data):
        """Negative test: Create user with missing username"""
        user_data = generate_user_data

        with allure.step("Attempt to create user without username"):
            response = user_api.create_user(
                username="",  # Empty username
                email=user_data["email"],
                password=user_data["password"],
                validate=False  # Skip validation to test API behavior
            )

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail with missing username"
            logger.info(f"✓ Missing username correctly rejected: {response.get('msg')}")

    @allure.title("Test create user with invalid email format - abnormal case")
    @allure.description("Attempt to create a user with an invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_invalid_email(self, generate_user_data):
        """Negative test: Create user with invalid email format"""
        user_data = generate_user_data
        invalid_emails = config_reader.get_test_data("invalid_emails")

        for invalid_email in invalid_emails[:2]:  # Test first 2 invalid emails
            with allure.step(f"Attempt to create user with invalid email: {invalid_email}"):
                response = user_api.create_user(
                    username=user_data["username"] + str(fake.random_int(1, 999)),
                    email=invalid_email,
                    password=user_data["password"],
                    validate=False  # Skip validation
                )

            with allure.step("Verify error response"):
                assert response["code"] != 200, f"Should fail with invalid email: {invalid_email}"
                logger.info(f"✓ Invalid email correctly rejected: {invalid_email}")

    @allure.title("Test create user with short password - abnormal case")
    @allure.description("Attempt to create a user with a password shorter than minimum length")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_short_password(self, generate_user_data):
        """Negative test: Create user with password too short"""
        user_data = generate_user_data

        with allure.step("Attempt to create user with short password"):
            response = user_api.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password="123",  # Too short (< 6 chars)
                validate=False
            )

        with allure.step("Verify error response"):
            assert response["code"] != 200, "Should fail with short password"
            logger.info(f"✓ Short password correctly rejected: {response.get('msg')}")

    @allure.title("Test create user with overly long username - edge case")
    @allure.description("Test system behavior with extremely long username")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_long_username(self, generate_user_data):
        """Edge case: Create user with very long username"""
        user_data = generate_user_data
        long_username = "a" * 256  # Very long username

        with allure.step(f"Attempt to create user with {len(long_username)}-character username"):
            response = user_api.create_user(
                username=long_username,
                email=user_data["email"],
                password=user_data["password"],
                validate=False
            )

        with allure.step("Verify response"):
            # Should either reject or truncate
            if response["code"] == 200:
                logger.info("✓ Long username accepted (API allows it)")
                if response.get("data"):
                    created_user_ids.append(response["data"]["id"])
            else:
                logger.info(f"✓ Long username rejected: {response.get('msg')}")

    @allure.title("Test create user with special characters in username - edge case")
    @allure.description("Test username with special characters")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_special_chars_username(self, generate_user_data):
        """Edge case: Create user with special characters in username"""
        user_data = generate_user_data
        special_username = "test@#$%^&*()"

        with allure.step(f"Attempt to create user with special chars username: {special_username}"):
            response = user_api.create_user(
                username=special_username,
                email=user_data["email"],
                password=user_data["password"],
                validate=False
            )

        with allure.step("Verify response"):
            if response["code"] == 200:
                logger.info("✓ Special characters in username accepted")
                if response.get("data"):
                    created_user_ids.append(response["data"]["id"])
            else:
                logger.info(f"✓ Special characters in username rejected: {response.get('msg')}")
