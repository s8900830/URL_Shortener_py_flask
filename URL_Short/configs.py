class Config:
    ENV = "development"
    DEBUG = True
    REDIS_URL = "redis://192.168.1.210:6379/0"
    SQLALCHEMY_DATABASE_URI = "mysql://admin:123456789@192.168.1.210:3306/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
