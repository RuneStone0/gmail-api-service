from flask import Flask, request, jsonify
from email_service import EmailService
from config import SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD
import os

app = Flask(__name__)

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

@app.route('/send-test-email', methods=['POST'])
def send_test_email():
    """Send test email endpoint"""
    try:
        success = email_service.send_test_email()
        
        if success:
            return jsonify({
                "message": "Test email sent successfully",
                "receiver": RECEIVER_EMAIL
            }), 200
        else:
            return jsonify({"error": "Failed to send test email"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run in debug mode if FLASK_ENV is set to development
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug) 