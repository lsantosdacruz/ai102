#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Azure App Service startup script
Runs on container startup
"""
import os
import sys

# Ensure the app directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run migrations or initialization if needed
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level="info"
    )
