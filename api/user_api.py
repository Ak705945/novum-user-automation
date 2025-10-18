from typing import Dict, Optional
import allure
from common.request_handler import request_handler
from common.logger import logger
from api.models import (
    CreateUserRequest, UpdateUserRequest,
    CreateUserResponse, GetUserResponse, UpdateUserResponse,
    DeleteUserResponse, BatchQueryResponse
)


class UserAPI:
    """User Management API client"""

    def __init__(self):
        self.base_endpoint = "/api/v1/users"

    @allure.step("Create user: {username}")
    def create_user(self, username: str, email: str, password: str,
                    validate: bool = True) -> Dict:
        """
        Create a new user

        Args:
            username: User's username
            email: User's email
            password: User's password
            validate: Whether to validate request with Pydantic

        Returns:
            Response JSON dict
        """
        payload = {
            "username": username,
            "email": email,
            "password": password
        }

        # Validate request if needed
        if validate:
            try:
                CreateUserRequest(**payload)
            except Exception as e:
                logger.warning(f"Request validation failed (expected for negative tests): {str(e)}")

        response = request_handler.post(self.base_endpoint, json=payload)
        return response.json()

    @allure.step("Get user details: user_id={user_id}")
    def get_user(self, user_id: int) -> Dict:
        """
        Get user details by ID

        Args:
            user_id: User ID

        Returns:
            Response JSON dict
        """
        endpoint = f"{self.base_endpoint}/{user_id}"
        response = request_handler.get(endpoint)
        return response.json()

    @allure.step("Update user email: user_id={user_id}, new_email={email}")
    def update_user_email(self, user_id: int, email: str,
                          validate: bool = True) -> Dict:
        """
        Update user's email address

        Args:
            user_id: User ID
            email: New email address
            validate: Whether to validate request with Pydantic

        Returns:
            Response JSON dict
        """
        payload = {"email": email}

        # Validate request if needed
        if validate:
            try:
                UpdateUserRequest(**payload)
            except Exception as e:
                logger.warning(f"Request validation failed (expected for negative tests): {str(e)}")

        endpoint = f"{self.base_endpoint}/{user_id}"
        response = request_handler.put(endpoint, json=payload)
        return response.json()

    @allure.step("Delete user: user_id={user_id}")
    def delete_user(self, user_id: int) -> Dict:
        """
        Delete a user by ID

        Args:
            user_id: User ID

        Returns:
            Response JSON dict
        """
        endpoint = f"{self.base_endpoint}/{user_id}"
        response = request_handler.delete(endpoint)
        return response.json()

    @allure.step("Batch query users: page={page}, size={size}, keyword={keyword}")
    def batch_query_users(self, page: int = 1, size: int = 10,
                          keyword: Optional[str] = None) -> Dict:
        """
        Batch query users with pagination and search

        Args:
            page: Page number (default: 1)
            size: Page size (default: 10)
            keyword: Search keyword (optional)

        Returns:
            Response JSON dict
        """
        params = {
            "page": page,
            "size": size
        }

        if keyword:
            params["keyword"] = keyword

        response = request_handler.get(self.base_endpoint, params=params)
        return response.json()


# Singleton instance
user_api = UserAPI()