from fastapi import APIRouter,HTTPException,status
from .. import schema, model,utilit
from ..database import main
import json
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


router = APIRouter(prefix="/user",tags=['User'])


@router.post("/",response_model=schema.userOut)
async def AddUser(user: schema.userIn):
    await main()
    
    hashed_password = utilit.hash(user.password)
    user.password = user.password = hashed_password

    created_user = await model.User(**user.dict()).create()
    
    return json.loads(json.dumps(jsonable_encoder(created_user)))


@router.get("/",response_model=list[schema.userOut])
async def GetAllUser():
    
    await main()
    users = await model.User.find_all().to_list()
    
    if users:
        return json.loads(json.dumps(jsonable_encoder(users)))
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    

@router.get("/{id}",response_model=schema.userOut)
async def GetById(id: str):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid ObjectID")
        
    
    await main()
    
    user = await model.User.find_one({"_id": ObjectId(id)})
    
    if user:
        
        return json.loads(json.dumps(jsonable_encoder(user)))
    
    else:
        raise HTTPException(status_code=(status.HTTP_404_NOT_FOUND),
                            detail=f"There's no Task found in this {id} ID")
        