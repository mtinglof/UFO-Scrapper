import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')  # Replace with a strong key

    # Database settings
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'your-rds-endpoint')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'your-username')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'your-password')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'your-database-name')
