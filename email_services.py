import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


class EmailService:

    def send_email(self, to_email: str, subject: str, body: str):
        print("📨 Email send called for:", to_email)

        if not settings.EMAIL_ENABLED:
            print("❌ Email disabled in settings")
            return

        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print("✅ Email sent successfully")

        except Exception as e:
            print("❌ Email sending failed:", e)


email_service = EmailService()
