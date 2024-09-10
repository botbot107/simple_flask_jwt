import yaml
import os

class Config:
    def __init__(self, config_file_path='config/config.yml'):
        # Load the YAML configuration file
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        # Load database settings
        self.DB_DRIVER = config_data['database']['driver']
        self.DB_HOST = config_data['database']['host']
        self.DB_PORT = config_data['database']['port']
        self.DB_NAME = config_data['database']['name']
        self.DB_USERNAME = config_data['database']['username']
        self.DB_PASSWORD = config_data['database']['password']
        self.DB_CONNECTION_STRING = (f'DRIVER={{{self.DB_DRIVER}}};'
                                     f'HOST={self.DB_HOST};'
                                     f'DATABASE={self.DB_NAME};'
                                     f'UID={self.DB_USERNAME};PWD={self.DB_PASSWORD}')

        # Load JWT settings
        self.JWT_SECRET_KEY = config_data['jwt']['secret_key']
        self.JWT_COOKIE_CSRF_PROTECT  = config_data['jwt'].get('cookie_csrf_protect', True)

        self.KEYCLOAK_SERVER = config_data['keycloak']['server']
        self.KEYCLOAK_REALM = config_data['keycloak']['realm']
        self.KEYCLOAK_CLIENT_ID = config_data['keycloak']['client_id']
        self.KEYCLOAK_CLIENT_SECRET = config_data['keycloak']['client_secret']
        self.KEYCLOAK_REDIRECT_URI = config_data['keycloak']['redirect_uri']


# Initialize Config globally
config = Config()
