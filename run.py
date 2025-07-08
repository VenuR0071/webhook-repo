# webhook-repo/run.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Must be imported after load_dotenv to access app.config
from app import create_app

# Get port from environment or default to 5000
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

app = create_app()

if __name__ == '__main__':
    # Use host and port from environment variables or defaults
    app.run(debug=True, host=HOST, port=PORT)