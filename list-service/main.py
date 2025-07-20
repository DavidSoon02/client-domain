from fastapi import FastAPI, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, User
from schemas import UserResponse, UserListResponse
from auth import verify_token
from typing import Optional
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="List Users Service")

@app.get("/users", response_model=UserListResponse)
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    query = db.query(User)
    
    if search:
        query = query.filter(
            (User.first_name.ilike(f"%{search}%")) |
            (User.last_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return UserListResponse(users=users, total=total)

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "list-users"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
