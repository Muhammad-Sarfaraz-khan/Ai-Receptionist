import asyncio
from app.config import settings

async def send_callback_reminder(contact_name: str, contact_phone: str, contact_email: str):
    await asyncio.sleep(900)  # 15 minutes

    # ✅ IMPORT ANDAR KARO (CIRCULAR FIX)
    from app.services.email_services import email_service

    email_service.send_email(
        to_email=settings.COMPANY_EMAIL,
        subject="⏰ Callback Reminder – New Lead",
        body=f"""
Reminder!

You have a pending lead callback.

Name: {contact_name}
Phone: {contact_phone}
Email: {contact_email}

Please call the client as soon as possible.
"""
    )
