import uuid
from typing import List, Dict, Optional
from openai import OpenAI

from app.config import settings
from app.utils.logger import setup_logger


class AIService:
    """Service for AI-powered conversation handling"""

    def __init__(self):
        # 🔹 Logger
        self.logger = setup_logger("AIService")

        self.model = settings.OPENAI_MODEL
        self.system_prompt = self._get_system_prompt()
        self.conversations: Dict[str, List[Dict]] = {}
        self.client = None

        self.logger.info("Initializing AIService")

        # 🔍 DEBUG: Check API key before initialization
        api_key = settings.OPENAI_API_KEY
        self.logger.info(f"API Key loaded: {bool(api_key)}")
        if api_key:
            self.logger.info(f"API Key starts with: {api_key[:10]}...")
            self.logger.info(f"API Key ends with: ...{api_key[-10:]}")
            self.logger.info(f"API Key length: {len(api_key)}")
        else:
            self.logger.warning("⚠️ API Key is EMPTY or None")

       # ✅ Safe OpenAI initialization
        if settings.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.logger.info("[OK] OpenAI client initialized successfully")
                self.logger.info(f"Using model: {self.model}")
            except Exception as e:
                self.logger.error("[ERROR] OpenAI initialization failed", exc_info=True)
        else:
            self.logger.warning("[WARNING] OPENAI_API_KEY missing – AI disabled")

    def _get_system_prompt(self) -> str:
        self.logger.info("Generating system prompt")

        return f"""
You are {settings.COMPANY_NAME}'s AI Receptionist.

You behave like a real human receptionist.
You are polite, friendly, proactive, and professional.

IMPORTANT RULES:
- Ask only ONE question at a time
- Keep responses short and clear

Services:
- Web Development
- Mobile Applications
- AI & Automation
- Cloud / IT Services

Company Details:
Name: {settings.COMPANY_NAME}
Email: {settings.COMPANY_EMAIL}
Phone: {settings.COMPANY_PHONE}
Hours: {settings.BUSINESS_HOURS}
"""

    def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        user_name: Optional[str] = None,
        user_email: Optional[str] = None
    ) -> Dict:
        self.logger.info("New chat request received")
        self.logger.info(f"User message: {message}")

        # ❌ AI disabled
        if not self.client:
            self.logger.warning("❌ Chat requested but AI is disabled (client is None)")
            return {
                "response": "AI service is currently unavailable. Please contact us directly.",
                "conversation_id": conversation_id,
                "suggested_actions": [],
                "requires_followup": False
            }

        # 🔁 Conversation ID
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            self.logger.info(f"Generated new conversation ID: {conversation_id}")

        # 🔁 Initialize conversation
        if conversation_id not in self.conversations:
            self.logger.info(f"Creating new conversation: {conversation_id}")
            self.conversations[conversation_id] = [
                {"role": "system", "content": self.system_prompt}
            ]

        # 🔹 User context
        user_context = ""
        if user_name:
            user_context += f"My name is {user_name}. "
        if user_email:
            user_context += f"My email is {user_email}. "

        self.conversations[conversation_id].append({
            "role": "user",
            "content": user_context + message
        })

        try:
            self.logger.info("Sending request to OpenAI")
            self.logger.info(f"Client exists: {self.client is not None}")
            self.logger.info(f"Model: {self.model}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversations[conversation_id]
            )

            ai_response = response.choices[0].message.content
            self.logger.info("✅ OpenAI response received successfully")

            self.conversations[conversation_id].append({
                "role": "assistant",
                "content": ai_response
            })

            suggested_actions = self._extract_suggested_actions(message)
            requires_followup = self._check_requires_followup(message)

            self.logger.info(f"Suggested actions: {suggested_actions}")
            self.logger.info(f"Requires follow-up: {requires_followup}")

            return {
                "response": ai_response,
                "conversation_id": conversation_id,
                "suggested_actions": suggested_actions,
                "requires_followup": requires_followup
            }

        except Exception as e:
            self.logger.error("❌ OpenAI request failed", exc_info=True)

            return {
                "response": (
                    "AI service temporarily unavailable. "
                    f"Please contact us at {settings.COMPANY_EMAIL}"
                ),
                "conversation_id": conversation_id,
                "suggested_actions": ["contact_support"],
                "requires_followup": True
            }

    def _extract_suggested_actions(self, user_message: str) -> List[str]:
        self.logger.info("Extracting suggested actions")

        msg = user_message.lower()
        actions = []

        if "service" in msg:
            actions.append("provide_service_info")
        if "appointment" in msg or "meeting" in msg:
            actions.append("schedule_appointment")
        if "contact" in msg:
            actions.append("provide_contact_info")

        return actions

    def _check_requires_followup(self, user_message: str) -> bool:
        urgent = ["urgent", "asap", "complaint"]
        result = any(word in user_message.lower() for word in urgent)

        self.logger.info(f"Follow-up required: {result}")
        return result

    def clear_conversation(self, conversation_id: str):
        self.logger.info(f"Clearing conversation: {conversation_id}")
        self.conversations.pop(conversation_id, None)


# ✅ SAFE Singleton
ai_service = AIService()