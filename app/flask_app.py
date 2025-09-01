from flask import Flask, request, jsonify
from .email_service import EmailService
from .config import SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD
from .test_routes import test_bp
import os

app = Flask(__name__)

# Register the test blueprint
app.register_blueprint(test_bp)

# Initialize email service
email_service = EmailService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "gmail-api-service"})

@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Send email endpoint
    
    Expected JSON payload:
    {
        "subject": "Email subject",
        "body": "Email body content",
        "receiver_email": "recipient@example.com",  # optional, uses default if not provided
        "is_html": false  # optional, if true, body is treated as HTML content
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate required fields
        if 'subject' not in data or 'body' not in data:
            return jsonify({"error": "Missing required fields: subject and body"}), 400
        
        subject = data['subject']
        body = data['body']
        receiver_email = data.get('receiver_email')  # Optional field
        is_html = data.get('is_html', False)  # Optional field, defaults to False
        
        # Send email
        success = email_service.send_email(subject, body, receiver_email, is_html)
        
        if success:
            return jsonify({
                "message": "Email sent successfully",
                "subject": subject,
                "receiver": receiver_email or RECEIVER_EMAIL,
                "content_type": "HTML" if is_html else "Plain Text"
            }), 200
        else:
            return jsonify({"error": "Failed to send email"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Flask app is now run via run.py entry point
# Use: python run.py 