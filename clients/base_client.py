import requests
import logging
from config.headers import DEFAULT_HEADERS

logger = logging.getLogger(__name__)


class BaseAPIClient:
    def __init__(self, base_url: str = None, timeout: int = 30):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = timeout
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        
        # Add default headers
        headers = kwargs.get('headers', {})
        for key, value in DEFAULT_HEADERS.items():
            headers.setdefault(key, value)
        kwargs['headers'] = headers
        
        logger.info(f"Making {method} request to {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"Response status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('PUT', endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('PATCH', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('DELETE', endpoint, **kwargs)

    def ping_health_check(self) -> bool:
        """Health check endpoint"""
        try:
            response = self._make_request('GET', '/ping')
            return response.status_code == 201
        except:
            return False
