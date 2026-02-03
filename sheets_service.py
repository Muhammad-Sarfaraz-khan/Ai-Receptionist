"""
Google Sheets Service for storing appointments, inquiries, and contacts
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
from datetime import datetime
from app.config import settings
import json


class SheetsService:
    """Service for interacting with Google Sheets"""
    
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets client"""
        try:
            if not settings.GOOGLE_SHEETS_CREDENTIALS_FILE:
                raise ValueError("GOOGLE_SHEETS_CREDENTIALS_FILE not set")
            
            # Define the scope
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            
            # Authenticate
            creds = Credentials.from_service_account_file(
                settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
                scopes=scope
            )
            
            self.client = gspread.authorize(creds)
            
            if settings.GOOGLE_SHEETS_SPREADSHEET_ID:
                self.spreadsheet = self.client.open_by_key(
                    settings.GOOGLE_SHEETS_SPREADSHEET_ID
                )
            else:
                # Create a new spreadsheet if ID not provided
                self.spreadsheet = self.client.create("AI Receptionist Data")
                settings.GOOGLE_SHEETS_SPREADSHEET_ID = self.spreadsheet.id
                
        except FileNotFoundError:
            print(f"Warning: Credentials file not found: {settings.GOOGLE_SHEETS_CREDENTIALS_FILE}")
            print("Google Sheets functionality will be disabled.")
        except Exception as e:
            print(f"Warning: Could not initialize Google Sheets: {str(e)}")
            print("Google Sheets functionality will be disabled.")
    
    def _get_or_create_worksheet(self, name: str, headers: List[str]) -> gspread.Worksheet:
        """Get existing worksheet or create a new one with headers"""
        if not self.spreadsheet:
            raise Exception("Google Sheets not initialized")
        
        try:
            worksheet = self.spreadsheet.worksheet(name)
            # Check if headers exist
            existing_headers = worksheet.row_values(1)
            if not existing_headers or existing_headers != headers:
                worksheet.insert_row(headers, 1)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = self.spreadsheet.add_worksheet(title=name, rows=1000, cols=20)
            worksheet.insert_row(headers, 1)
        
        return worksheet
    
    def save_appointment(self, appointment_data: Dict) -> str:
        """Save an appointment to Google Sheets"""
        if not self.spreadsheet:
            return "sheets_disabled"
        
        try:
            headers = [
                "ID", "Name", "Email", "Phone", "Company", "Date", "Time",
                "Duration", "Purpose", "Status", "Notes", "Created At", "Updated At"
            ]
            
            worksheet = self._get_or_create_worksheet("Appointments", headers)
            
            row = [
                appointment_data.get("id", ""),
                appointment_data.get("contact", {}).get("name", ""),
                appointment_data.get("contact", {}).get("email", ""),
                appointment_data.get("contact", {}).get("phone", ""),
                appointment_data.get("contact", {}).get("company", ""),
                appointment_data.get("scheduled_date", ""),
                appointment_data.get("scheduled_time", ""),
                appointment_data.get("duration", ""),
                appointment_data.get("purpose", ""),
                appointment_data.get("status", "pending"),
                appointment_data.get("notes", ""),
                appointment_data.get("created_at", ""),
                appointment_data.get("updated_at", "")
            ]
            
            worksheet.append_row(row)
            return "success"
            
        except Exception as e:
            print(f"Error saving appointment to sheets: {str(e)}")
            return f"error: {str(e)}"
    
    def save_inquiry(self, inquiry_data: Dict) -> str:
        """Save an inquiry to Google Sheets"""
        if not self.spreadsheet:
            return "sheets_disabled"
        
        try:
            headers = [
                "ID", "Name", "Email", "Phone", "Company", "Type", "Subject",
                "Description", "Priority", "Status", "Contact Method", "Created At", "Updated At"
            ]
            
            worksheet = self._get_or_create_worksheet("Inquiries", headers)
            
            row = [
                inquiry_data.get("id", ""),
                inquiry_data.get("contact", {}).get("name", ""),
                inquiry_data.get("contact", {}).get("email", ""),
                inquiry_data.get("contact", {}).get("phone", ""),
                inquiry_data.get("contact", {}).get("company", ""),
                inquiry_data.get("inquiry_type", ""),
                inquiry_data.get("subject", ""),
                inquiry_data.get("description", ""),
                inquiry_data.get("priority", ""),
                inquiry_data.get("status", "open"),
                inquiry_data.get("preferred_contact_method", ""),
                inquiry_data.get("created_at", ""),
                inquiry_data.get("updated_at", "")
            ]
            
            worksheet.append_row(row)
            return "success"
            
        except Exception as e:
            print(f"Error saving inquiry to sheets: {str(e)}")
            return f"error: {str(e)}"
    
    def save_contact(self, contact_data: Dict) -> str:
        """Save a contact to Google Sheets"""
        if not self.spreadsheet:
            return "sheets_disabled"
        
        try:
            headers = [
                "Name", "Email", "Phone", "Company", "Notes", "Created At"
            ]
            
            worksheet = self._get_or_create_worksheet("Contacts", headers)
            
            row = [
                contact_data.get("name", ""),
                contact_data.get("email", ""),
                contact_data.get("phone", ""),
                contact_data.get("company", ""),
                contact_data.get("notes", ""),
                datetime.now().isoformat()
            ]
            
            worksheet.append_row(row)
            return "success"
            
        except Exception as e:
            print(f"Error saving contact to sheets: {str(e)}")
            return f"error: {str(e)}"
    
    def get_appointments(self, limit: int = 100) -> List[Dict]:
        """Get recent appointments from Google Sheets"""
        if not self.spreadsheet:
            return []
        
        try:
            worksheet = self.spreadsheet.worksheet("Appointments")
            records = worksheet.get_all_records()
            return records[-limit:] if len(records) > limit else records
        except Exception as e:
            print(f"Error getting appointments from sheets: {str(e)}")
            return []
    
    def get_inquiries(self, limit: int = 100) -> List[Dict]:
        """Get recent inquiries from Google Sheets"""
        if not self.spreadsheet:
            return []
        
        try:
            worksheet = self.spreadsheet.worksheet("Inquiries")
            records = worksheet.get_all_records()
            return records[-limit:] if len(records) > limit else records
        except Exception as e:
            print(f"Error getting inquiries from sheets: {str(e)}")
            return []


# Global instance
sheets_service = SheetsService()
