import json
import os
from typing import Dict, Any


class ConfigReader:
    """Read and manage configuration from JSON files"""

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                       'config', 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)

    def get_environment(self) -> str:
        """Get current environment from ENV variable, default to 'test'"""
        return os.getenv('TEST_ENV', 'test')

    def get_base_url(self) -> str:
        """Get base URL for current environment"""
        env = self.get_environment()
        return self._config['environments'][env]['base_url']

    def get_timeout(self) -> int:
        """Get request timeout for current environment"""
        env = self.get_environment()
        return self._config['environments'][env].get('timeout', 30)

    def get_retry_config(self) -> Dict[str, int]:
        """Get retry configuration"""
        env = self.get_environment()
        return {
            'retry_times': self._config['environments'][env].get('retry_times', 3),
            'retry_delay': self._config['environments'][env].get('retry_delay', 1)
        }

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self._config.get('logging', {})

    def get_default_headers(self) -> Dict[str, str]:
        """Get default headers for requests"""
        return self._config.get('default_headers', {})

    def get_test_data(self, key: str = None) -> Any:
        """Get test data from test_data.json"""
        test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                      'config', 'test_data.json')
        with open(test_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if key:
            return data.get(key)
        return data


# Singleton instance
config_reader = ConfigReader()