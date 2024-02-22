import os

ENV = os.environ.get("Flask_ENV", "development")
DEBUG = os.environ.get("DEBUG", True)
REDIS_URL = os.environ.get("REDIS_URL", "redis://192.168.1.210:6379/0")
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "mysql://admin:123456789@192.168.1.210:3306/test")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS", False)

# ENV = "development"
# DEBUG = True
# REDIS_URL = "redis://192.168.1.210:6379/0"
# SQLALCHEMY_DATABASE_URI = "mysql://admin:123456789@192.168.1.210:3306/test"
# SQLALCHEMY_TRACK_MODIFICATIONS = False
