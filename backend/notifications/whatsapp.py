import logging
from core.config import settings
import httpx

logger = logging.getLogger("cara.notifications.whatsapp")

async def send_whatsapp_alert(phone: str, template_name: str, parameters: list):
    """
    Sends WhatsApp templated messages via Meta Cloud API or Twilio.
    Used for sending the initial temporary password and caregiver alerts.
    """
    logger.info(f"Sending WhatsApp template {template_name} to {phone}")
    
    # Example using Meta Graph API layout
    url = f"https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": { "code": "en" },
            "components": [
                {
                    "type": "body",
                    "parameters": parameters
                }
            ]
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return True
            logger.error(f"WhatsApp Error: {response.text}")
            return False
    except Exception as e:
        logger.error(f"WhatsApp Exception: {str(e)}")
        return False
