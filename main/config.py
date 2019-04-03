class Config:
    SECRET_KEY = 'any secret string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTS_PER_PAGE = 15


