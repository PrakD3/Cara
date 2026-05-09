import logging
from core.config import settings
import httpx

logger = logging.getLogger("cara.ivr.exotel")

async def trigger_ivr_call(phone: str, flow_id: str, dynamic_data: dict):
    """
    Triggers an outbound IVR call to the patient using Exotel.
    """
    logger.info(f"Triggering IVR call to {phone} with flow {flow_id}")
    url = f"https://api.exotel.com/v1/Accounts/{settings.IVR_SID}/Calls/connect.json"
    
    auth = (settings.IVR_SID, settings.IVR_AUTH_TOKEN)
    data = {
        "From": phone,
        "To": phone, # Usually a virtual number
        "CallerId": "YOUR_EXOTEL_VIRTUAL_NUMBER",
        "Url": f"{settings.IVR_WEBHOOK_URL}?patient_flow={flow_id}",
        "CallType": "trans"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, auth=auth, data=data)
            if response.status_code == 200:
                logger.info("Call triggered successfully")
                return response.json()
            else:
                logger.error(f"Exotel trigger failed: {response.text}")
                return None
    except Exception as e:
        logger.error(f"IVR Exception: {str(e)}")
        return None
