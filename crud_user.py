import boto3
from encoder import CustomeEncoder
import json
import logging
logger=logging.getLogger()
logger.setLevel(logging.INFO)
from time import gmtime, strftime


dynamodbTableName= 'users' # dynamodbtablename
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
endpoint = '/user'  #apiend point for Accessing data resourse name

def lambda_handler(event,context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
     
    #for fetching single specific user record using id
    if httpMethod == getMethod and path == endpoint:
        requestBody = json.loads(event['body'])
        response = getuser(requestBody['userId'])
    
    # for creating New user record
    elif httpMethod == postMethod and path == endpoint:
        response = createuser(json.loads(event['body']))

    # for updating record  
    elif httpMethod == patchMethod and path == endpoint:   # New code for updateuser
        requestBody = json.loads(event['body'])
        response = updateuser(requestBody['userId'],requestBody)
    
    # for deleting record using id
    elif httpMethod == deleteMethod and path == endpoint:
        requestBody = json.loads(event['body'])
        response = deleteuser(requestBody['userId'])

    else:
        response = buildResponse(404,'User Not Found !!')
    
    return response

# crud functions here 

def getuser(userId):
    try:
        response = table.get_item(
            Key= {
                'userId':userId
            }
        )
        if 'Item' in response:
            return buildResponse(200,response['Item'])
        else:
            return buildResponse(404,{'Message':'UserId : %s not found' %userId})
    except:
        logger.exception('something went unexpected !!')


def createuser(requestBody):
    requestBody["Record-created-time"]=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item' : requestBody
        }
        return buildResponse(200,body)
    except:
        logger.exception('something went unexpected !!')

def updateuser(userId,updateValue):
    updateValue["Record-updated-time"]=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    try:
        response = table.put_item(Item=updateValue)
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes' : updateValue
        }
        return buildResponse(200,body)
    except:
        logger.exception('something went unexpected !!')

def deleteuser(userId):
    try:
        response = table.delete_item(
            Key= {
                'userId':userId
            },
            ReturnValues='ALL_OLD'
        )  
        body = {
            'Operation': 'DELETE',
            'Message':'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200,body)
    except:
        logger.exception('something went unexpected !!')



# Custom JsonResponse Creater for requests
def buildResponse(statusCode,body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Cotent-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body,cls=CustomeEncoder)
        
    return response


