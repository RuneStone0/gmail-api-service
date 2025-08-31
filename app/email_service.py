import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD


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

    def send_email(self, subject, body, receiver_email=None):
        """
        Send an email with the specified subject and body.
        
        Args:
            subject (str): Email subject
            body (str): Email body content
            receiver_email (str, optional): Override default receiver email
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create the email
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = receiver_email or self.receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

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

    def send_test_email(self):
        """
        Send a test email with default subject and body.
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        subject = "Test Email"
        body = "This is a test email sent programmatically from Python!"
        return self.send_email(subject, body) 