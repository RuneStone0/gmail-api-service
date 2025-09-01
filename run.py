#!/usr/bin/env python3
"""
Entry point for running the Flask application directly.
This file allows you to run the app with: python run.py
"""

import os
from app.flask_app import app

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run in debug mode if FLASK_ENV is set to development
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
