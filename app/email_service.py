import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD


class EmailService:
    def __init__(self, sender_email=None, receiver_email=None, app_password=None):
        """
        Initialize EmailService with email credentials.
        If not provided, will use values from config.
        """
        self.sender_email = sender_email or SENDER_EMAIL
        self.receiver_email = receiver_email or RECEIVER_EMAIL
        self.app_password = app_password or APP_PASSWORD
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, subject, body, receiver_email=None, is_html=False):
        """
        Send an email with the specified subject and body.
        
        Args:
            subject (str): Email subject
            body (str): Email body content
            receiver_email (str, optional): Override default receiver email
            is_html (bool): If True, body is treated as HTML content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create the email
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = receiver_email or self.receiver_email
            msg["Subject"] = subject
            
            # Set content type based on is_html parameter
            content_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, content_type))

            # Connect to Gmail's SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, receiver_email or self.receiver_email, msg.as_string())
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_html_email(self, subject, html_body, receiver_email=None):
        """
        Send an HTML email with the specified subject and HTML body.
        
        Args:
            subject (str): Email subject
            html_body (str): HTML email body content
            receiver_email (str, optional): Override default receiver email
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        return self.send_email(subject, html_body, receiver_email, is_html=True)

    def send_test_email(self):
        """
        Send a test email with default subject and body.
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        subject = "Test Email"
        body = "This is a test email sent programmatically from Python!"
        return self.send_email(subject, body)

    def send_test_html_email(self):
        """
        Send a test HTML email with default subject and HTML body.
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        subject = "Test HTML Email"
        html_body = """
        <html>
        <head>
            <title>Test HTML Email</title>
        </head>
        <body>
            <h1 style="color: #2c3e50;">Hello from Gmail API Service!</h1>
            <p style="color: #34495e; font-size: 16px;">
                This is a <strong>test HTML email</strong> sent programmatically from Python!
            </p>
            <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="color: #e74c3c;">Features:</h3>
                <ul style="color: #2c3e50;">
                    <li>HTML formatting support</li>
                    <li>Styled content</li>
                    <li>Professional appearance</li>
                </ul>
            </div>
            <p style="color: #7f8c8d; font-style: italic;">
                Sent via Gmail API Service
            </p>
        </body>
        </html>
        """
        return self.send_html_email(subject, html_body) 