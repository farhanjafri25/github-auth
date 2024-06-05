import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from fastapi.exceptions import HTTPException
from fastapi.requests import Request


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyAJbdK4nbX2M7ldNXWGqaAD5mUg0qNIDtI",
  "authDomain": "authenticate-19076.firebaseapp.com",
  "projectId": "authenticate-19076",
  "storageBucket": "authenticate-19076.appspot.com",
  "messagingSenderId": "803756540388",
  "appId": "1:803756540388:web:eb98b6d93139ae55a1c7f1",
  "measurementId": "G-62FQ03C3V6",
  "databaseURL": ""
}
 
firebase = pyrebase.initialize_app(firebaseConfig)


def createUser(userData):
    try:
        user = auth.create_user(
            email = userData.email,
            password = userData.password
        )
        print('user', user)
        if user is not None:
            return 'Account created successfully'
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code = 400,
            detail = "Account already exists"
        )
        
def loginUser(userData):
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email = userData.email,
            password = userData.password
        )
        
        token = user['idToken']
        return token
    except: 
        raise HTTPException(
            status_code = 400,
            detail= "Invalid credentials"
        )
        
def verifyToken(request: Request):
    headers = request.headers
    token = headers.get('authorization')
    if token is None:
        raise HTTPException(status_code= 401,  detail= "Authorization is required")
    token = token.split(" ")[1]
    try:
        decoded = auth.verify_id_token(token)
        print('decoded tokne', decoded)
        return decoded
    except Exception as e:
        raise HTTPException(status_code = 401, detail = 'Unauthorized')
    
    