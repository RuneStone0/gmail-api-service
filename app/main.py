from email_service import EmailService


def main():
    # Create email service instance
    email_service = EmailService()
    
    # Send test email
    if email_service.send_test_email():
        print("Email sent successfully!")
    else:
        print("Failed to send email.")

    # Send test HTML email
    if email_service.send_test_html_email():
        print("HTML email sent successfully!")
    else:
        print("Failed to send HTML email.")


if __name__ == "__main__":
    main()