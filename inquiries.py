"""
Inquiries router for handling customer inquiries
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import InquiryRequest, Inquiry
from app.services.sheets_service import sheets_service
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/inquiries", response_model=Inquiry)
async def create_inquiry(request: InquiryRequest):
    """
    Create a new inquiry
    
    - **contact**: Contact information
    - **inquiry_type**: Type of inquiry (support, sales, technical, general, appointment)
    - **subject**: Subject of the inquiry
    - **description**: Detailed description
    - **priority**: Priority level (low, medium, high, urgent)
    """
    try:
        inquiry_id = str(uuid.uuid4())
        now = datetime.now()
        
        inquiry = Inquiry(
            id=inquiry_id,
            contact=request.contact,
            inquiry_type=request.inquiry_type,
            subject=request.subject,
            description=request.description,
            priority=request.priority,
            status="open",
            preferred_contact_method=request.preferred_contact_method,
            created_at=now,
            updated_at=now
        )
        
        # Save to Google Sheets
        inquiry_data = inquiry.model_dump()
        inquiry_data["created_at"] = now.isoformat()
        inquiry_data["updated_at"] = now.isoformat()
        sheets_service.save_inquiry(inquiry_data)
        
        # Also save contact
        contact_data = request.contact.model_dump()
        contact_data["notes"] = f"Inquiry: {request.subject}"
        sheets_service.save_contact(contact_data)
        
        return inquiry
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating inquiry: {str(e)}")


@router.get("/inquiries", response_model=list[Inquiry])
async def get_inquiries(limit: int = 50):
    """Get list of inquiries"""
    try:
        inquiries_data = sheets_service.get_inquiries(limit=limit)
        
        inquiries = []
        for data in inquiries_data:
            try:
                inquiry = Inquiry(
                    id=data.get("ID", ""),
                    contact={
                        "name": data.get("Name", ""),
                        "email": data.get("Email", ""),
                        "phone": data.get("Phone"),
                        "company": data.get("Company"),
                        "notes": data.get("Notes")
                    },
                    inquiry_type=data.get("Type", "general"),
                    subject=data.get("Subject", ""),
                    description=data.get("Description", ""),
                    priority=data.get("Priority", "medium"),
                    status=data.get("Status", "open"),
                    preferred_contact_method=data.get("Contact Method"),
                    created_at=datetime.fromisoformat(data.get("Created At", datetime.now().isoformat())),
                    updated_at=datetime.fromisoformat(data.get("Updated At", datetime.now().isoformat()))
                )
                inquiries.append(inquiry)
            except Exception as e:
                print(f"Error parsing inquiry: {str(e)}")
                continue
        
        return inquiries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting inquiries: {str(e)}")


@router.get("/inquiries/{inquiry_id}", response_model=Inquiry)
async def get_inquiry(inquiry_id: str):
    """Get a specific inquiry by ID"""
    try:
        inquiries = await get_inquiries(limit=1000)
        for inquiry in inquiries:
            if inquiry.id == inquiry_id:
                return inquiry
        
        raise HTTPException(status_code=404, detail="Inquiry not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting inquiry: {str(e)}")
