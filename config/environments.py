import os


class Config:
    ENVIRONMENTS = {
        'prod': {
            'base_url': 'https://restful-booker.herokuapp.com'
        },
        'dev': {
            'base_url': 'https://dev.restful-booker.herokuapp.com'
        },
        'staging': {
            'base_url': 'https://staging.restful-booker.herokuapp.com'
        }
    }
    
    @classmethod
    def get_base_url(cls) -> str:
        """Get base URL for current environment"""
        env = os.getenv('TEST_ENV', 'prod')
        if env not in cls.ENVIRONMENTS:
            raise ValueError(f"Unknown environment: {env}. Available: {list(cls.ENVIRONMENTS.keys())}")
        return cls.ENVIRONMENTS[env]['base_url']
    
    @classmethod
    def get_auth_credentials(cls) -> dict:
        """Get authentication credentials"""
        return {
            'username': os.getenv('API_USERNAME', 'admin'),
            'password': os.getenv('API_PASSWORD', 'password123')
        }
