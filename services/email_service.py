class EmailService:
    def __init__(self, provider: str = "smtp"):
        self.provider = provider

    def send_verification_email(self, to_email: str, token: str):
        print(f"Sending verification email to {to_email} with token {token}")
        # Implement provider specific sending logic here

    def send_password_reset_email(self, to_email: str, token: str):
        print(f"Sending reset email to {to_email}")

    def send_welcome_email(self, to_email: str):
        print(f"Sending welcome email to {to_email}")

email_service = EmailService()
