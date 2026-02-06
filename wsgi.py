"""
WSGI entry point for Azure App Service
"""
from app.main import app

if __name__ == "__main__":
    app.run()
