# gmail-api-service
A straightforward API endpoint for sending emails through Gmail.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
   - Copy `env.example` to `.env`
   - Fill in your actual values in the `.env` file:
     ```
     SENDER_EMAIL=your_email@gmail.com
     RECEIVER_EMAIL=recipient@example.com
     APP_PASSWORD=your_app_password
     ```

### Getting Your Gmail App Password

To use this service, you'll need a Gmail app password (not your regular Gmail password):

1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Enable 2-Step Verification if not already enabled
3. In "Security," navigate to "App passwords"
4. Select "Mail" as the app and generate a 16-character app password
5. Save this password securely and use it as your `APP_PASSWORD` in the `.env` file

3. Run the application:
```bash
python app/main.py
```

## Docker Deployment

### Using Docker Compose (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop the service
docker-compose down
```

### Using Docker directly
```bash
# Build the image
docker build -t gmail-api-service .

# Run the container
docker run -p 5000:5000 --env-file .env gmail-api-service

# Run with custom environment variables
docker run -p 5000:5000 \
  -e SENDER_EMAIL=your_email@gmail.com \
  -e RECEIVER_EMAIL=recipient@example.com \
  -e APP_PASSWORD=your_app_password \
  gmail-api-service
```

## Usage

### Python Class Usage
```python
from email_service import EmailService

# Create email service with default config
email_service = EmailService()

# Send test email
email_service.send_test_email()

# Send custom email to specific recipient
email_service.send_email("Custom Subject", "Custom message body", "recipient@example.com")
```

## API Endpoints

### Start the Flask Server
```bash
python app/flask_app.py
```

The server will start on `http://localhost:5000` by default.

### Available Endpoints

#### Health Check
```bash
GET /health
```
Returns service health status.

#### Send Email
```bash
POST /send-email
Content-Type: application/json

{
    "subject": "Email Subject",
    "body": "Email content",
    "receiver_email": "recipient@example.com"  # optional
}
```

#### Send Test Email
```bash
POST /send-test-email
```
Sends a test email with default subject and body.

### Example API Usage

#### Using curl
```bash
# Send custom email
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Hello from API",
    "body": "This email was sent via the Flask API"
  }'

# Send test email
curl -X POST http://localhost:5000/send-test-email

# Check health
curl http://localhost:5000/health
```

#### Using Python requests
```python
import requests

# Send email
response = requests.post('http://localhost:5000/send-email', json={
    'subject': 'Hello from Python',
    'body': 'This is a test email'
})

print(response.json())
```

## Environment Variables

- `SENDER_EMAIL`: Your Gmail address
- `RECEIVER_EMAIL`: Recipient's email address
- `APP_PASSWORD`: Your Gmail app password (not your regular password)

## Security Note

Never commit your actual `.env` file to version control.
