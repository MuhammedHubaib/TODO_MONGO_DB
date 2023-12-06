from beanie import Document

class User(Document):
    
    name: str
    email: str
    password: str
    
class Task(Document):
    
    task: str
    description: str
    date_and_time: str
    completed: bool
    user_id: str 