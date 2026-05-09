"""
Push Notification Service — handles FCM (Firebase Cloud Messaging) for Expo mobile
and standard device push notifications.
"""
import logging
import httpx
from core.config import settings

logger = logging.getLogger("cara.notifications.push")

FCM_URL = "https://fcm.googleapis.com/fcm/send"


async def send_push_notification(device_token: str, title: str, body: str, data: dict = None):
    """
    Sends a push notification to a device via Firebase Cloud Messaging.
    Works with Expo React Native apps using FCM tokens.
    """
    if not settings.FCM_SERVER_KEY:
        logger.warning("FCM_SERVER_KEY not set. Skipping push notification.")
        return False

    payload = {
        "to": device_token,
        "notification": {
            "title": title,
            "body": body,
            "sound": "default",
        },
        "data": data or {},
        "priority": "high",
    }

    headers = {
        "Authorization": f"key={settings.FCM_SERVER_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(FCM_URL, json=payload, headers=headers)
            if response.status_code == 200:
                logger.info(f"Push sent to {device_token[:20]}...")
                return True
            logger.error(f"FCM push failed: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Push notification exception: {str(e)}")
        return False


async def send_caregiver_alert(caregiver_device_token: str, patient_name: str, missed_count: int):
    """
    Sends a HIPAA-safe caregiver alert about patient missed doses.
    PHI is deliberately minimal — no diagnosis, no medication names.
    """
    title = "Health Companion Alert"
    body = f"{patient_name} may need your attention. Please check in with them."

    return await send_push_notification(
        device_token=caregiver_device_token,
        title=title,
        body=body,
        data={"type": "CAREGIVER_ALERT", "missed_count": str(missed_count)}
    )


async def send_doctor_alert(doctor_device_token: str, patient_name: str, risk_level: str):
    """
    Sends a HIPAA-safe doctor alert about high-risk patient status.
    """
    title = "CARA Risk Alert"
    body = f"Patient {patient_name} has been flagged as {risk_level} risk. Please review."

    return await send_push_notification(
        device_token=doctor_device_token,
        title=title,
        body=body,
        data={"type": "DOCTOR_RISK_ALERT", "risk_level": risk_level}
    )
