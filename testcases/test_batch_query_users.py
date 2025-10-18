import pytest
import allure
from faker import Faker
from api.user_api import user_api
from common.assertions import assertions
from common.config_reader import config_reader
from common.logger import logger
from testcases.conftest import created_user_ids


@allure.feature("User Management")
@allure.story("Batch Query Users")
class TestBatchQueryUsers:
    """Test cases for Batch Query Users API"""

    @allure.title("Test batch query users with default pagination - normal case")
    @allure.description("Query users with default page and size parameters")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_batch_query_users_normal(self, create_test_user):
        """Positive test: Batch query with default pagination"""
        # Create test user to ensure at least one exists
        user_data = create_test_user

        with allure.step("Query users with default pagination"):
            response = user_api.batch_query_users(page=1, size=10)

        with allure.step("Verify response structure"):
            assertions.assert_response_code(response, 200)
            assertions.assert_response_message(response, "success")
            assertions.assert_field_exists(response, "data")
            assertions.assert_not_none(response["data"], "Query data")

            data = response["data"]
            assertions.assert_field_exists(data, "total")
            assertions.assert_field_exists(data, "list")

            # Verify list structure
            assert isinstance(data["list"], list), "List should be an array"
            logger.info(f"✓ Batch query successful: total={data['total']}, returned={len(data['list'])}")

    @allure.title("Test batch query users with keyword search - normal case")
    @allure.description("Query users using keyword filter")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_batch_query_users_with_keyword(self, create_test_user):
        """Positive test: Batch query with keyword search"""
        user_data = create_test_user
        keyword = user_data["username"][:5]  # Use part of username as keyword

        with allure.step(f"Query users with keyword: {keyword}"):
            response = user_api.batch_query_users(page=1, size=10, keyword=keyword)

        with allure.step("Verify search results"):
            assertions.assert_response_code(response, 200)
            assertions.assert_response_message(response, "success")

            data = response["data"]
            assert isinstance(data["list"], list), "List should be an array"

            # Verify keyword appears in results
            if len(data["list"]) > 0:
                found = any(keyword.lower() in user["username"].lower() for user in data["list"])
                assert found, f"Keyword '{keyword}' should appear in search results"
                logger.info(f"✓ Keyword search successful: found {len(data['list'])} matches")
            else:
                logger.warning("No results found for keyword search")

    @allure.title("Test batch query users with custom page size - normal case")
    @allure.description("Query users with different page sizes")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_custom_page_size(self):
        """Positive test: Batch query with custom page size"""
        page_size = 5

        with allure.step(f"Query users with page size: {page_size}"):
            response = user_api.batch_query_users(page=1, size=page_size)

        with allure.step("Verify page size constraint"):
            assertions.assert_response_code(response, 200)

            data = response["data"]
            returned_count = len(data["list"])

            # Returned count should not exceed requested page size
            assert returned_count <= page_size, \
                f"Returned count ({returned_count}) should not exceed page size ({page_size})"
            logger.info(f"✓ Page size constraint verified: requested={page_size}, returned={returned_count}")

    @allure.title("Test batch query users with invalid page number - abnormal case")
    @allure.description("Attempt to query with invalid page number (negative or zero)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_invalid_page(self):
        """Negative test: Query with invalid page number"""
        invalid_page = -1

        with allure.step(f"Attempt to query with invalid page: {invalid_page}"):
            response = user_api.batch_query_users(page=invalid_page, size=10)

        with allure.step("Verify error response"):
            # API should either reject or default to valid page
            if response["code"] != 200:
                logger.info(f"✓ Invalid page correctly rejected: {response.get('msg')}")
            else:
                logger.info("✓ Invalid page handled with default value")

    @allure.title("Test batch query users with invalid page size - abnormal case")
    @allure.description("Attempt to query with invalid page size (zero or negative)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_invalid_size(self):
        """Negative test: Query with invalid page size"""
        invalid_size = 0

        with allure.step(f"Attempt to query with invalid size: {invalid_size}"):
            response = user_api.batch_query_users(page=1, size=invalid_size)

        with allure.step("Verify error response"):
            if response["code"] != 200:
                logger.info(f"✓ Invalid size correctly rejected: {response.get('msg')}")
            else:
                logger.info("✓ Invalid size handled with default value")

    @allure.title("Test batch query users with non-existent keyword - abnormal case")
    @allure.description("Query with keyword that matches no users")
    @allure.severity(allure.severity_level.NORMAL)
    def test_batch_query_users_no_results(self):
        """Negative test: Query with keyword that returns no results"""
        non_existent_keyword = "nonexistent_user_12930"

        with allure.step(f"Query with non-existent keyword: {non_existent_keyword}"):
            response = user_api.batch_query_users(page=1, size=10, keyword=non_existent_keyword)

        with allure.step("Verify empty results"):
            assertions.assert_response_code(response, 200)

            data = response["data"]
            assert data["total"] == 0 or len(data["list"]) == 0, \
                "Should return empty results for non-existent keyword"
            logger.info(f"✓ No results correctly returned for non-existent keyword")

    @allure.title("Test batch query users with page beyond total pages - edge case")
    @allure.description("Query a page number that exceeds total available pages")
    @allure.severity(allure.severity_level.MINOR)
    def test_batch_query_users_page_beyond_total(self):
        """Edge case: Query page beyond total pages"""
        large_page = 99999

        with allure.step(f"Query page far beyond total: page={large_page}"):
            response = user_api.batch_query_users(page=large_page, size=10)

        with allure.step("Verify empty or error response"):
            assertions.assert_response_code(response, 200)

            data = response["data"]
            # Should return empty list or handle gracefully
            assert len(data["list"]) == 0, "Should return empty list for page beyond total"
            logger.info(f"✓ Page beyond total handled correctly: returned empty list")

    @allure.title("Test batch query users with very large page size - edge case")
    @allure.description("Test system behavior with extremely large page size")
    @allure.severity(allure.severity_level.MINOR)
    def test_batch_query_users_large_page_size(self):
        """Edge case: Query with very large page size"""
        large_size = 10000

        with allure.step(f"Query with very large page size: {large_size}"):
            response = user_api.batch_query_users(page=1, size=large_size)

        with allure.step("Verify response handling"):
            if response["code"] == 200:
                data = response["data"]
                returned_count = len(data["list"])
                # System might cap the maximum page size
                logger.info(f"✓ Large page size handled: requested={large_size}, returned={returned_count}")
            else:
                logger.info(f"✓ Large page size rejected: {response.get('msg')}")

    @allure.title("Test batch query users with empty keyword - edge case")
    @allure.description("Test behavior with empty string as keyword")
    @allure.severity(allure.severity_level.MINOR)
    def test_batch_query_users_empty_keyword(self):
        """Edge case: Query with empty keyword"""
        with allure.step("Query with empty keyword"):
            response = user_api.batch_query_users(page=1, size=10, keyword="")

        with allure.step("Verify response"):
            assertions.assert_response_code(response, 200)
            # Empty keyword should return all users (same as no keyword)
            logger.info(f"✓ Empty keyword handled: returned {len(response['data']['list'])} users")

