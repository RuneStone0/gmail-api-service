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

### Using GitHub Container Registry (Recommended)

The Docker image is automatically built and pushed to GitHub Container Registry on every push to main branch and release tags.

```bash
# Pull the latest image
docker pull ghcr.io/yourusername/gmail-api-service:main

# Pull a specific version
docker pull ghcr.io/yourusername/gmail-api-service:v1.0.0

# Run the container
docker run -p 5000:5000 --env-file .env ghcr.io/yourusername/gmail-api-service:main
```

### Using Docker Compose with GitHub Container Registry
```yaml
# docker-compose.yml
version: '3.8'
services:
  gmail-api-service:
    image: ghcr.io/yourusername/gmail-api-service:main
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: unless-stopped
```

```bash
# Run with Docker Compose
docker-compose up -d
```

### Local Development with Docker Compose
```bash
# Build and run locally
docker-compose up --build

# Run in background
docker-compose up -d

# Stop the service
docker-compose down
```

### Using Docker directly (local build)
```bash
# Build the image locally
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

## Security Note

Never commit your actual `.env` file to version control.

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

# Send HTML email
html_content = """
<html>
<body>
    <h1>Hello!</h1>
    <p>This is an <strong>HTML email</strong> with formatting.</p>
</body>
</html>
"""
email_service.send_html_email("HTML Email", html_content, "recipient@example.com")

# Send email with HTML flag
email_service.send_email("HTML Email", html_content, "recipient@example.com", is_html=True)
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
    "receiver_email": "recipient@example.com",  # optional
    "is_html": false  # optional, if true, body is treated as HTML content
}
```

#### Send Test Email
```bash
POST /send-test-email
```
Sends a test email with default subject and body.

#### Send Test HTML Email
```bash
POST /send-test-html-email
```
Sends a test HTML email with styled content and formatting.

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

# Send HTML email
curl -X POST http://localhost:5000/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "HTML Email from API",
    "body": "<h1>Hello!</h1><p>This is an <strong>HTML email</strong>!</p>",
    "is_html": true
  }'

# Send test email
curl -X POST http://localhost:5000/send-test-email

# Send test HTML email
curl -X POST http://localhost:5000/send-test-html-email

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

# Send HTML email
html_content = """
<html>
<body>
    <h1 style="color: #2c3e50;">Hello from Python!</h1>
    <p style="color: #34495e;">This is an <strong>HTML email</strong> with styling.</p>
</body>
</html>
"""

response = requests.post('http://localhost:5000/send-email', json={
    'subject': 'HTML Email from Python',
    'body': html_content,
    'is_html': True
})

print(response.json())
```

## Environment Variables

- `SENDER_EMAIL`: Your Gmail address
- `RECEIVER_EMAIL`: Recipient's email address
- `APP_PASSWORD`: Your Gmail app password (not your regular password)

## Security Note

Never commit your actual `.env` file to version control.
