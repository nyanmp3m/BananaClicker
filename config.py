import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'first_DB', 'db', 'users1.db')