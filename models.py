from pydantic import BaseModel

class InputLink(BaseModel):
    url: str
    
class SignUpSchema(BaseModel):
    email: str
    password: str
    
class LoginSchema(BaseModel):
    email: str
    password: str