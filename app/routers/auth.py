from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database, schemas, models, utils, oauth2
router = APIRouter(tags=['authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credential:schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credential.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return {"access_token": access_token , "token_type": "bearer"}

