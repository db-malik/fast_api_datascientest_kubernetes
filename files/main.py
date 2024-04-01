from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from sqlalchemy.engine import create_engine
import os
import base64


# creating a FastAPI server
server = FastAPI(title='User API')


encoded_password = os.environ.get('MYSQL_ROOT_PASSWORD')
decoded_password = base64.b64decode(encoded_password).decode('utf-8')


# creating a connection to the database
mysql_url = 'mysql-container:3306'
mysql_user = 'root'
mysql_password = decoded_password #'datascientest1234'  
database_name = 'Main'

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# creating the connection
mysql_engine = create_engine(connection_url)


# creating a User class
class User(BaseModel):
    user_id: int = 0
    username: str = 'daniel'
    email: str = 'daniel@datascientest.com'


@server.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})



@server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1

@server.get('/database_credentials')
async def get_database_credentials():
    return {
        "username": mysql_user,
        "password": mysql_password,
        "database_name": database_name,
        "url"=mysql_url,
    }


@server.get('/test_db_connection')
async def test_db_connection():
  try:
    with mysql_engine.connect() as connection:
      # Do nothing, just open and close the connection to test
      pass
    return {"message": "Database connection successful"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@server.get('/users')
async def get_users():
    try:
        with mysql_engine.connect() as connection:
            results = connection.execute('SELECT * FROM Users;')

        results = [
            User(
                user_id=i[0],
                username=i[1],
                email=i[2]
            ) for i in results.fetchall()]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    with mysql_engine.connect() as connection:
        results = connection.execute(
            'SELECT * FROM Users WHERE Users.id = {};'.format(user_id))

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail='Unknown User ID')
    else:
        return results[0]
