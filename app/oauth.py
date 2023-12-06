from jose import jwt,JWTError
from datetime import timedelta,datetime
from . import schema,model
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from .database import main
from bson import ObjectId
from .config import settings



oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes

def create_token(data: dict):
    to_encode = data.copy()
    
    expire_time = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    
    if "user_id" in to_encode:
        to_encode["user_id"] = str(to_encode["user_id"])
        
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentails_exception):
    
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = payload.get('user_id')
        
        if id is None:
            raise credentails_exception
        token_data= schema.token(id=id)
        
    except JWTError:
        raise credentails_exception
    
    return token_data

async def get_current_user(token: str= Depends(oauth2_schema)):
    
    await main()
    credentails_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Couldn't validate the Credentials",
                                          headers={'WWW-Authenticate':'Bearer'})
    
    token = verify_token(token,credentails_exception)
    #user =  await model.User.find_one({"_id":token.id})
    user = model.User.find_one({"_id": ObjectId(token.id)})

    if not user:
        raise credentails_exception
    
    user_dict = dict(await user)

    return user_dict

     