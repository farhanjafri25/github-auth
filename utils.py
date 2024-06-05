import hashlib
import json

def addIdentifiertoData(data):
    if isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = addIdentifiertoData(item)
    elif isinstance(data, dict):
        print(data)
        identifier = generateIdentifier(data)
        data['identifier'] = identifier
        # print('data processed', data)
        # print()
        return data
    else:
        print(f"Unexpected type: {type(data)}")
    return data

def generateIdentifierForRepo(repoUrl):
    hashed_value = hashlib.sha1(repoUrl.encode()).hexdigest()
    print('Identifier for repo', hashed_value)
    return hashed_value

        
def generateIdentifier(object): 
    json_string = json.dumps(object, sort_keys=True)
    hashed_value = hashlib.sha1(json_string.encode()).hexdigest()
    print(hashed_value)
    return hashed_value


def flatten_array(arr):
    result = []
    for element in arr:
        if isinstance(element, list):
            result.extend(flatten_array(element))
        else:
            result.append(element)
    return result

