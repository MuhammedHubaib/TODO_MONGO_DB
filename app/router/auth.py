from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import model,utilit,oauth
from ..database import main

router = APIRouter()


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    await main()
    user_a = await model.User.find_one(model.User.name == user_credentials.username)
    
    if not user_a:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    if not utilit.verify(user_credentials.password, user_a.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invaild credentials")
    
    access_token=oauth.create_token(data={"user_id":user_a.id})
    return {"token":access_token,"token_type":"bearer"}