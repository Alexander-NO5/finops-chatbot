import smtplib
import ssl
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from app.config import SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT, SECRET_KEY

serializer = URLSafeTimedSerializer(SECRET_KEY)

def send_verification_email(full_name, receiver_email):
    token = serializer.dumps(receiver_email, salt="email-confirmation-salt")
    verification_link = f"http://localhost:5000/verify/{token}"

    msg = EmailMessage()
    msg["Subject"] = "Verify Your FinOpsBot Account"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content(
        f"Hello {full_name},\n\n"
        f"Click the link below to verify your email:\n{verification_link}\n\n"
        "If you did not request this, please ignore the email."
    )

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Verification email sent to {receiver_email}.")
        return token  # Optional for testing
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None

def send_password_reset_email(full_name, receiver_email):
    token = serializer.dumps(receiver_email, salt="reset-password-salt")
    reset_link = url_for('reset_password_token', token=token, _external=True)

    msg = EmailMessage()
    msg["Subject"] = "Reset Your FinOpsBot Password"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content(
        f"Hi {full_name},\n\nClick the link below to reset your password:\n{reset_link}\n\n"
        "If you didn't request a password reset, just ignore this email."
    )

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Password reset email sent to {receiver_email}.")
    except Exception as e:
        print(f"Failed to send reset email: {e}")
