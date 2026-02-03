from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import AppointmentRequest, Appointment, AppointmentStatus
from app.services.reminder_service import send_callback_reminder
from app.services.sheets_service import sheets_service
from app.services.email_services import email_service
from app.config import settings
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/appointments", response_model=Appointment)
async def create_appointment(
    request: AppointmentRequest,
    background_tasks: BackgroundTasks
):
    try:
        appointment_id = str(uuid.uuid4())
        now = datetime.now()

        # ================= CREATE APPOINTMENT OBJECT =================
        appointment = Appointment(
            id=appointment_id,
            contact=request.contact,
            scheduled_date=request.preferred_date,
            scheduled_time=request.preferred_time,
            duration=request.duration,
            purpose=request.purpose,
            status=AppointmentStatus.PENDING,
            notes=request.notes,
            created_at=now,
            updated_at=now
        )

        # ================= SAVE APPOINTMENT TO GOOGLE SHEETS =================
        appointment_data = {
            "id": appointment_id,
            "contact": {
                "name": request.contact.name,
                "email": request.contact.email,
                "phone": request.contact.phone,
                "company": request.contact.company
            },
            "scheduled_date": request.preferred_date,
            "scheduled_time": request.preferred_time,
            "duration": request.duration,
            "purpose": request.purpose,
            "status": "pending",
            "notes": request.notes,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

        result = sheets_service.save_appointment(appointment_data)
        print("📊 Appointment Sheet Result:", result)

        # ================= SAVE CONTACT TO GOOGLE SHEETS =================
        contact_data = {
            "name": request.contact.name,
            "email": request.contact.email,
            "phone": request.contact.phone,
            "company": request.contact.company,
            "notes": f"Appointment request: {request.purpose}"
        }

        contact_result = sheets_service.save_contact(contact_data)
        print("📊 Contact Sheet Result:", contact_result)

        # ================= EMAIL 1: CUSTOMER AUTO-REPLY =================
        background_tasks.add_task(
            email_service.send_email,
            request.contact.email,
            f"Thanks for contacting {settings.COMPANY_NAME}",
            f"""
Hello {request.contact.name},

Thank you for contacting {settings.COMPANY_NAME}.
We have received your appointment request.

Our team will call you shortly to confirm.

📞 Phone: {settings.COMPANY_PHONE}
📧 Email: {settings.COMPANY_EMAIL}

Best regards,
{settings.COMPANY_NAME} Team
"""
        )

        # ================= EMAIL 2: COMPANY NOTIFICATION =================
        background_tasks.add_task(
            email_service.send_email,
            settings.COMPANY_EMAIL,
            "📥 New Appointment Lead Received",
            f"""
New appointment request received.

Name: {request.contact.name}
Email: {request.contact.email}
Phone: {request.contact.phone}
Company: {request.contact.company}

Preferred Date: {request.preferred_date}
Preferred Time: {request.preferred_time}
Purpose: {request.purpose}

Please follow up with the customer.
"""
        )

        # ================= EMAIL 3: CALLBACK REMINDER (15 MIN) =================
        background_tasks.add_task(
            send_callback_reminder,
            request.contact.name,
            request.contact.phone,
            request.contact.email
        )

        return appointment

    except Exception as e:
        print("❌ Appointment Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to create appointment. Please try again."
        )
