import os

class Config:
    DB_HOSt = os.getenv("DB_HOST","my.database.com")
    DB_USERNAME= os.getenv("DB_USERNAME")
    DB_PASSWORD= os.getenv("DB_PASSWORD")
    DB_NAME= ...
    RATE_LIMIT = ...