import requests
import time
import json
import allure
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from common.logger import logger
from common.config_reader import config_reader


class RequestHandler:
    """Handle HTTP requests with retry mechanism and logging"""

    def __init__(self):
        self.base_url = config_reader.get_base_url()
        self.timeout = config_reader.get_timeout()
        self.default_headers = config_reader.get_default_headers()
        retry_config = config_reader.get_retry_config()

        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=retry_config['retry_times'],
            backoff_factor=retry_config['retry_delay'],
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _log_request(self, method: str, url: str, headers: Dict, data: Any):
        """Log request details"""
        logger.info(f"→ {method} {url}")
        logger.debug(f"Headers: {json.dumps(headers, indent=2)}")
        if data:
            logger.debug(f"Request Body: {json.dumps(data, indent=2)}")

    def _log_response(self, response: requests.Response):
        """Log response details"""
        logger.info(f"← Status: {response.status_code}")
        try:
            logger.debug(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except:
            logger.debug(f"Response Body: {response.text}")

    def _attach_to_allure(self, method: str, url: str, headers: Dict,
                          request_body: Any, response: requests.Response):
        """Attach request/response details to Allure report"""
        # Request details
        request_info = f"Method: {method}\nURL: {url}\nHeaders: {json.dumps(headers, indent=2)}"
        if request_body:
            request_info += f"\nBody: {json.dumps(request_body, indent=2)}"
        allure.attach(request_info, "Request Details", allure.attachment_type.TEXT)

        # Response details
        response_info = f"Status Code: {response.status_code}\n"
        try:
            response_info += f"Body: {json.dumps(response.json(), indent=2)}"
        except:
            response_info += f"Body: {response.text}"
        allure.attach(response_info, "Response Details", allure.attachment_type.TEXT)

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Generic request method with retry and logging

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        headers = {**self.default_headers, **kwargs.pop('headers', {})}
        data = kwargs.get('json', kwargs.get('data'))

        # Log request
        self._log_request(method, url, headers, data)

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )

            # Log response
            self._log_response(response)

            # Attach to Allure
            self._attach_to_allure(method, url, headers, data, response)

            return response

        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {str(e)}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET request"""
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST request"""
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT request"""
        return self.request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        return self.request('DELETE', endpoint, **kwargs)


# Singleton instance
request_handler = RequestHandler()