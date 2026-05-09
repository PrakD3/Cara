from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.domain_schemas import LoginRequest, Token
from models.database import get_db
from models.domain import User
from auth.jwt import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}
