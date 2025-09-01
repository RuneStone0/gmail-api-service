from flask import Blueprint, request, jsonify
from .email_service import EmailService
from .config import RECEIVER_EMAIL

# Create a Blueprint for test routes
test_bp = Blueprint('test', __name__, url_prefix='/test')

# Initialize email service
email_service = EmailService()

@test_bp.route('/send-email', methods=['POST'])
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

@test_bp.route('/send-html-email', methods=['POST'])
def send_test_html_email():
    """Send test HTML email endpoint"""
    try:
        success = email_service.send_test_html_email()
        
        if success:
            return jsonify({
                "message": "Test HTML email sent successfully",
                "receiver": RECEIVER_EMAIL,
                "content_type": "HTML"
            }), 200
        else:
            return jsonify({"error": "Failed to send test HTML email"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@test_bp.route('/send-multiple-recipients', methods=['POST'])
def send_test_multiple_recipients():
    """Send test email to multiple recipients endpoint"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get recipients from request or use default
        recipients = data.get('recipients', RECEIVER_EMAIL)
        subject = data.get('subject', 'Test Multiple Recipients')
        body = data.get('body', 'This is a test email sent to multiple recipients!')
        is_html = data.get('is_html', False)
        
        # Send email
        success = email_service.send_email(subject, body, recipients, is_html)
        
        if success:
            return jsonify({
                "message": "Test email sent successfully to multiple recipients",
                "subject": subject,
                "recipients": recipients,
                "content_type": "HTML" if is_html else "Plain Text"
            }), 200
        else:
            return jsonify({"error": "Failed to send test email"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
