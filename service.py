from fastapi import Depends, FastAPI, HTTPException, status
from extract import parse_codebase
from models import InputLink
import os
from github_func import clone_repo, cleanup_temp_dir
from utils import addIdentifiertoData, flatten_array, generateIdentifierForRepo
from db_execution import saveRepoLink, getFileIdByName, saveFileData, saveClassData, saveFunctionData, getFunctionById, fetchFunctionAndId
import json



def saveData(inputUrl):
    print('url received', inputUrl)
    clone_dir = os.path.join(os.getcwd(), "cloned_repo")
    repo_path = clone_repo(inputUrl,clone_dir)
    if(repo_path):
        repoIdentifier = generateIdentifierForRepo(inputUrl)
        saveRepoLink(inputUrl, repoIdentifier)
    try:
        metadata_list = parse_codebase(repo_path)
        metadataObj = addIdentifiertoData(metadata_list)
        arrayObject = flatten_array(metadataObj)
        json_data = arrayObject
        print('arrayObject', json_data)
        print()
        for item in json_data:
            file_id = getFileIdByName(item['file_name'], repoIdentifier)
            if file_id is None:
                item['repo_id'] = repoIdentifier
                file_id = saveFileData(item)
            item['file_id'] = file_id
            class_id = saveClassData(item)
            item['class_id'] = class_id
            function_id = saveFunctionData(item)
            print(function_id)
        cleanup_temp_dir(clone_dir)
        return inputUrl
    except Exception as e: 
        print("error", e)
    return {"data": inputUrl}


def getFunctionCode(identifier):
    print('identifier', identifier)
    try:
        function_code = getFunctionById(identifier)
        return function_code
    except Exception as e:
        print("error getFunctionCode", e)
        return e
    
def listFunctions(page, pageSize):
    try:
        res = fetchFunctionAndId(page, pageSize)
        response = {
            "docs": res,
            "nextPage" : page + 1 if len(res) >= pageSize else None,
        }
        return response
    except Exception as e:
        print("error")
        raise HTTPException(status_code = 400, detail = "Something went wrong")
        
    