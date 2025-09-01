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

    def _parse_receiver_emails(self, receiver_email):
        """
        Parse receiver email(s) into a list.
        If receiver_email is a string, split by comma and strip whitespace.
        If receiver_email is already a list, return as is.
        
        Args:
            receiver_email: String (comma-separated) or list of email addresses
            
        Returns:
            list: List of email addresses
        """
        if receiver_email is None:
            receiver_email = self.receiver_email
            
        if isinstance(receiver_email, str):
            # Split by comma and strip whitespace from each email
            return [email.strip() for email in receiver_email.split(',') if email.strip()]
        elif isinstance(receiver_email, list):
            return receiver_email
        else:
            # Fallback to single email in a list
            return [str(receiver_email)]

    def send_email(self, subject, body, receiver_email=None, is_html=False):
        """
        Send an email with the specified subject and body.
        
        Args:
            subject (str): Email subject
            body (str): Email body content
            receiver_email (str or list, optional): Override default receiver email(s).
                                                   Can be comma-separated string or list.
            is_html (bool): If True, body is treated as HTML content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Parse receiver emails
            receiver_emails = self._parse_receiver_emails(receiver_email)
            
            # Create the email
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(receiver_emails)  # Join multiple emails with comma
            msg["Subject"] = subject
            
            # Set content type based on is_html parameter
            content_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, content_type))

            # Connect to Gmail's SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS
            server.login(self.sender_email, self.app_password)
            
            # Send to all recipients
            server.sendmail(self.sender_email, receiver_emails, msg.as_string())
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
            receiver_email (str or list, optional): Override default receiver email(s).
                                                   Can be comma-separated string or list.
            
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