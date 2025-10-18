import logging
import os
from datetime import datetime
from common.config_reader import ConfigReader


class Logger:
    """Custom logger with configurable levels and file output"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        config = ConfigReader().get_logging_config()

        # Create logs directory if not exists
        log_dir = os.path.dirname(config.get('file', 'logs/test_execution.log'))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        self.logger = logging.getLogger('APIAutomation')
        self.logger.setLevel(config.get('level', 'INFO'))

        # File handler
        log_file = config.get('file', 'logs/test_execution.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(config.get('format',
                                                 '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


# Singleton instance
logger = Logger().get_logger()