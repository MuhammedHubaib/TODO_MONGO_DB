from fastapi import APIRouter,HTTPException,status,Depends,Response
from .. import schema, model,oauth
from ..database import main
import json
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


router = APIRouter(prefix="/task",tags=['Task'])

@router.post("/", response_model=schema.task)
async def add_task(task: schema.taskIn, current_user = Depends(oauth.get_current_user)):
    await main()
    created_task = await model.Task(user_id = str(current_user["id"]),**task.dict()).create()
    return json.loads(json.dumps(jsonable_encoder(created_task)))



@router.get("/",response_model= list[schema.task])
async def get_all():
    
    await main()
    tasks_cursor = await model.Task.find_all().to_list()
    
    if tasks_cursor:
        return json.loads(json.dumps(jsonable_encoder(tasks_cursor)))
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



@router.get("/{id}",response_model=schema.task)
async def get_task_by_id(id: str,current_user: str = Depends(oauth.get_current_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid ObjectID")
    
    await main()
    task = await model.Task.find_one({"_id": ObjectId(id)})

    if not task:
        raise HTTPException(status_code=(status.HTTP_404_NOT_FOUND),
                            detail=f"There's no Task found in this {id} ID")
        
    if str(task.user_id) != str(current_user["id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to perform this action")
    
    return jsonable_encoder(task)

        




@router.put("/{id}", response_model=schema.task)
async def UpdateTask(id: str, updated_task: schema.taskIn,current_user: str = Depends(oauth.get_current_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid ObjectID")
        
    await main()
    
    existing_task = await model.Task.find_one({"_id": ObjectId(id)})
    
    if not existing_task:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
       
    # Create an instance of the model and update its fields
    existing_task_data = jsonable_encoder(existing_task.dict())
    updated_task_data = {**existing_task_data, **updated_task.dict()}
    
     
    if str(existing_task.user_id) != str(current_user["id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to perform this action")
                
    # Update the task in the database
    task_updated=  await existing_task.update({"$set": updated_task_data})

    return jsonable_encoder(task_updated)

   

  
@router.delete("/{id}",response_model=schema.task)
async def DeleteTask(id: str, current_user: str = Depends(oauth.get_current_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid ObjectID")
        
        
    await main()
    task = await model.Task.find_one({"_id": ObjectId(id)})
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    if str(task.user_id) != str(current_user["id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to perform this action")
    
    
    response = Response(status_code=status.HTTP_204_NO_CONTENT, content=None)
    return response