from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.sheets_service import sheets_service
from app.services.email_services import email_service
from app.config import settings

router = APIRouter()

@router.post("/contact")
async def create_contact(data: dict, background_tasks: BackgroundTasks):
    try:
        contact_data = {
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone", ""),
            "company": data.get("company", ""),
            "notes": data.get("message", "")
        }

        result = sheets_service.save_contact(contact_data)
        print("📊 Contact Sheet Result:", result)

        # Customer auto-reply
        background_tasks.add_task(
            email_service.send_email,
            data.get("email"),
            f"Thanks for contacting {settings.COMPANY_NAME}",
            "Thanks for contacting us. Our team will call you shortly."
        )

        # Company notification
        background_tasks.add_task(
            email_service.send_email,
            settings.COMPANY_EMAIL,
            "📥 New Contact Lead",
            f"Name: {data.get('name')}\nEmail: {data.get('email')}"
        )

        return {"status": "success"}

    except Exception as e:
        print("❌ Contact Error:", e)
        raise HTTPException(status_code=500, detail="Contact submission failed")
