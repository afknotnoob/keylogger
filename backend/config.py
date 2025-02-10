import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/key_logger'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = secrets.token_hex(16)