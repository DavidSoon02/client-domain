from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, User
from schemas import DeleteResponse
from auth import verify_token
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Delete User Service")

@app.delete("/users/{user_id}", response_model=DeleteResponse)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return DeleteResponse(
        message="User deleted successfully",
        deleted_user_id=user_id
    )

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "delete-user"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
