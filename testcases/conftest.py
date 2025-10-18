from typing import List

import allure
import pytest

from api.user_api import user_api
from common.config_reader import config_reader
from common.logger import logger

# Track created user IDs for cleanup
created_user_ids: List[int] = []


@pytest.fixture(scope="function")
def generate_user_data():
    """Generate unique user data for testing"""
    return config_reader.get_test_data("valid_user")


@pytest.fixture(scope="function")
def create_test_user(generate_user_data):
    """Create a test user and return user data with ID"""
    user_data = generate_user_data
    response = user_api.create_user(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"]
    )

    if response.get("code") == 200 and response.get("data"):
        user_id = response["data"]["id"]
        user_data["id"] = user_id
        created_user_ids.append(user_id)
        logger.info(f"Test user created: ID={user_id}, username={user_data['username']}")
        yield user_data
    else:
        pytest.fail(f"Failed to create test user: {response}")


@pytest.fixture(scope="function", autouse=False)
def cleanup_user(request):
    """Cleanup user after test (optional fixture)"""
    user_id = None

    def set_user_id(uid):
        nonlocal user_id
        user_id = uid

    yield set_user_id

    # Cleanup after test
    if user_id:
        try:
            user_api.delete_user(user_id)
            logger.info(f"Cleaned up test user: ID={user_id}")
            if user_id in created_user_ids:
                created_user_ids.remove(user_id)
        except Exception as e:
            logger.warning(f"Failed to cleanup user {user_id}: {str(e)}")


def pytest_sessionfinish(session, exitstatus):
    """Cleanup all created users at the end of test session"""
    logger.info(f"Test session finished. Cleaning up {len(created_user_ids)} test users...")

    for user_id in created_user_ids[:]:  # Create a copy to iterate
        try:
            user_api.delete_user(user_id)
            logger.info(f"✓ Cleaned up user: ID={user_id}")
            created_user_ids.remove(user_id)
        except Exception as e:
            logger.warning(f"✗ Failed to cleanup user {user_id}: {str(e)}")

    if created_user_ids:
        logger.warning(f"Failed to cleanup {len(created_user_ids)} users: {created_user_ids}")
    else:
        logger.info("All test users cleaned up successfully")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach test result to Allure report"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            allure.attach(
                f"Test failed: {report.longreprtext}",
                "Failure Details",
                allure.attachment_type.TEXT
            )