from connection import connection
from datetime import datetime, date

def serialize_datetime(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj

class ValidationError(Exception):
    pass

class QueryError(Exception):
    pass

def saveRepoLink(repourl, repoId):
    try:
        cursor = connection.cursor()
        query = """
        INSERT into repo_urls(id, url) VALUES (%s, %s)
        """
        cursor.execute(query, [repoId, repourl,])
        connection.commit()
        cursor.close()
        return repoId
    except Exception as e:
        print('error saving repo data', e)
        connection.rollback()
        return


def saveClassData(body):
    try:
        cursor = connection.cursor()
        print("THIS IS BODY saveClassData: " , body)
        query = """
        INSERT INTO classes (class_name, file_id) VALUES(%s,%s) RETURNING id
        """
        insertData = (body.get('class_name'), body.get('file_id'))
        cursor.execute(query, insertData)
        class_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return class_id,
    except Exception as e:
        connection.rollback()
        print('This is original exception, ', e)
        raise ValidationError('Unable to save to class Table')
    
def saveFileData(body):
    try: 
        cursor = connection.cursor()
        print("THIS IS BODY saveFileData: " , body)
        query = """
        INSERT INTO file(file_name, repo_id) VALUES(%s, %s) RETURNING id
        """
        insertData = (body.get('file_name'), body.get('repo_id'))
        cursor.execute(query, insertData)
        file_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        return file_id
    except Exception as e:
        connection.rollback()
        print('Error saving file data', e)
        raise ValidationError('Error saving file data')
    
def saveFunctionData(body): 
    try:
        cursor = connection.cursor()
        print("Body recieved saveFunctionData", body)
        query = """
        INSERT INTO function(function_id, function_body, class_id, file_id, function_name) VALUES (%s,%s,%s,%s,%s)
        """
        insertData = (body.get('identifier'), body.get('code'), body.get('class_id'), body.get('file_id'), body.get('function_name'))
        cursor.execute(query, insertData)
        connection.commit()
        cursor.close()
        return "Function saved successfully"
    except Exception as e:
        connection.rollback()
        print('Error saving function', e)
        raise ValidationError('Error saving function')


def getFunctionById(functionId):
    try:
        print('functionId recieved', functionId)
        cursor = connection.cursor()
        query = """
        SELECT function_body from function where function_id = %s and is_deleted = false
        """
        cursor.execute(query, [functionId,])
        function_body = cursor.fetchone()
        if function_body is None: 
            return None
        column_names = [desc[0] for desc in cursor.description]
        function_data_serialzable = {}
        for name, value in zip(column_names, function_body):
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            function_data_serialzable[name] = value
        return function_data_serialzable
    except Exception as e:
        connection.rollback()
        return f"Error: {str(e)}"
    
    
def getRepoIdWithFileName(repo_id, file_name):
    try: 
        print('getRepoIdWithFileName body', repo_id, file_name)
        cursor = connection.cursor()
        query = """
        select id from file where repo_id = %s and file_name = %s
        """
        cursor.execute(query,[repo_id, file_name,])
        data = cursor.fetchone()
        return data
    except Exception as e:
        connection.rollback()
        return f"Error: {str(e)}"
    
def getFileIdByName(file_name, repo_id):
    try:
        cursor = connection.cursor()
        query = """
        SELECT id from file where file_name = %s and repo_id = %s
        """
        cursor.execute(query, [file_name, repo_id,])
        data = cursor.fetchone()
        print('getFileIdByName', data)
        return data
    except Exception as e:
        connection.rollback()
        return f"Error fetching data: {str(e)}"
    
def fetchFunctionAndId(page=1, pageSize=10):
    print(page, pageSize)
    try:
        cursor = connection.cursor()
        query = """
        Select function_id, function_name from function order by created_at desc offset %s limit %s 
        """
        cursor.execute(query,[(page - 1) * pageSize, pageSize,])
        functionData = cursor.fetchall()
        print('functionData', functionData)
        return functionData
    except Exception as e:
        print('error', e)
        return f"Error fetching data: {str(e)}"

        