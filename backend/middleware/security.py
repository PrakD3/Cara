from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.domain import AuditLog
from datetime import datetime
import time

class SecurityAndAuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Inject Strict Security Headers (HIPAA/GDPR compliance baseline)
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        # Audit Logging for specific modifying paths
        if request.method in ["POST", "PUT", "DELETE"] and "/api/" in request.url.path:
            db: Session = SessionLocal()
            try:
                # Naive user extraction, actual auth handled via dependencies
                audit = AuditLog(
                    action=request.method,
                    entity=request.url.path,
                    entity_id=0, # Placeholder, captured in exact route ideally
                    timestamp=datetime.utcnow()
                )
                db.add(audit)
                db.commit()
            except Exception:
                pass
            finally:
                db.close()
                
        return response
