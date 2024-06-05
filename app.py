from fastapi import Depends, FastAPI, HTTPException, status
from models import InputLink, SignUpSchema, LoginSchema
from service import saveData, getFunctionById, listFunctions
from response_interceptor import format_response
from firebase_init import createUser, loginUser, verifyToken
from fastapi.requests import Request



def create_app():
    app = FastAPI()
    
    @app.get("/test")
    async def test():
        return {"hello": "world"}
    
    @app.post("/signup")
    async def createAccount(user: SignUpSchema):
        print("user.email", user.email)
        print("user.password", user.password)
        res = createUser(user)
        return format_response(201, res)
      
    
    @app.post('/login')
    async def loginAccount(user: LoginSchema):
        res = loginUser(user)
        return format_response(201, res)
    
    @app.get('/list-functions')
    async def fetchFunctionList(page = 1, pageSize= 10, user: dict = Depends(verifyToken)):
        res = listFunctions(page, pageSize)
        return format_response(200, res)
    
    @app.post('/repo')
    async def fetchUrlData(input_link: InputLink, user: dict = Depends(verifyToken)):
        print('url received', input_link.url)
        res = saveData(input_link.url)
        return format_response(201, res)
    
    
    @app.get("/fetch-code")
    async def fetchCode(identifier: str, user: dict = Depends(verifyToken)):
        res = getFunctionById(identifier)
        return format_response(200, res)
    
     
    return app