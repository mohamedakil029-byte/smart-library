"""Application Configuration"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///library_requests.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Request defaults
    REQUEST_TIMEOUT = timedelta(days=30)
    APPROVAL_REQUIRED_THRESHOLD = 5  # Number of items requiring approval
    
    # Email/Notification settings
    NOTIFICATION_ENABLED = True
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@library.com')
    
    # ServiceNow Integration
    SERVICENOW_URL = os.getenv('SERVICENOW_URL', 'https://dev.service-now.com')
    SERVICENOW_USER = os.getenv('SERVICENOW_USER', 'integration_user')
    SERVICENOW_PASS = os.getenv('SERVICENOW_PASS', '')
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
