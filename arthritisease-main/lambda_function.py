import json
import boto3
import uuid
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

# JSON Encoder
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Connect to DynamoDB tables
dynamodb = boto3.resource('dynamodb')
comments_table = dynamodb.Table('ArthritEase_Comments')

# Dynamic CORS headers function
def cors_headers(origin=None):
    allowed_origins = [
        'https://arthritisease.org',
        'http://localhost:5173',
        'http://localhost:3000'
    ]
    
    # If no origin provided, return default configuration
    if not origin:
        return {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:5173',  # Default for development
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key,X-Amz-Date,Authorization,X-Api-Stage,X-Requested-With,Accept,Origin',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600',
            'Vary': 'Origin'
        }
    
    # If origin is in allowed list, return corresponding configuration
    if origin in allowed_origins:
        return {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key,X-Amz-Date,Authorization,X-Api-Stage,X-Requested-With,Accept,Origin',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600',
            'Vary': 'Origin'
        }
    
    # If it's a development environment with different port
    if origin.startswith('http://localhost:'):
        return {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key,X-Amz-Date,Authorization,X-Api-Stage,X-Requested-With,Accept,Origin',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600',
            'Vary': 'Origin'
        }
    
    # Default to production environment configuration
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': allowed_origins[0],
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE',
        'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key,X-Amz-Date,Authorization,X-Api-Stage,X-Requested-With,Accept,Origin',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '3600',
        'Vary': 'Origin'
    }

def lambda_handler(event, context):
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', '')
    path = event.get('path', '/')
    origin = event.get('headers', {}).get('origin', '')

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers(origin),
            'body': json.dumps({'message': 'CORS preflight passed'})
        }

    if http_method == 'POST' and path.rstrip('/') == '/sessions':
        return create_session(event, context)
    elif http_method == 'GET' and path.startswith('/sessions/'):
        return get_session(event, context)
    elif http_method == 'POST' and path.rstrip('/') == '/comments':
        return create_comment(event, context, origin)
    elif http_method == 'GET' and path.rstrip('/') == '/comments':
        return get_comments(event, context, origin)
    elif http_method == 'PUT' and path.startswith('/comments/'):
        return update_comment(event, context, origin)
    elif http_method == 'DELETE' and path.startswith('/comments/'):
        return delete_comment(event, context, origin)
    else:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Invalid request method or path'})
        }

def create_comment(event, context, origin):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing request body'})
        }

    body = json.loads(event['body'])
    required_fields = ['topicId', 'sessionId', 'content', 'anonymousName']
    for field in required_fields:
        if field not in body:
            return {
                'statusCode': 400,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': f'Missing required field: {field}'})
            }

    if len(body['content']) > 1000:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Comment content too long'})
        }

    current_time = datetime.now().isoformat()
    expiration_time = (datetime.now() + timedelta(days=30)).timestamp()

    item = {
        'commentId': str(uuid.uuid4()),
        'topicId': body['topicId'],
        'sessionId': body['sessionId'],
        'content': body['content'],
        'anonymousName': body['anonymousName'],
        'createdAt': current_time,
        'updatedAt': current_time,
        'expiresAt': int(expiration_time),
        'likes': 0,
        'isDeleted': False
    }

    try:
        comments_table.put_item(Item=item)
        return {
            'statusCode': 200,
            'headers': cors_headers(origin),
            'body': json.dumps(item, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': str(e)})
        }

def get_comments(event, context, origin):
    if 'queryStringParameters' not in event or 'topicId' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing topicId parameter'})
        }

    topic_id = event['queryStringParameters']['topicId']

    try:
        response = comments_table.scan(
            FilterExpression=Attr('topicId').eq(topic_id) & Attr('isDeleted').eq(False)
        )
        return {
            'statusCode': 200,
            'headers': cors_headers(origin),
            'body': json.dumps(response['Items'], cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': str(e)})
        }

def update_comment(event, context, origin):
    if 'body' not in event or 'pathParameters' not in event:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing request body or commentId'})
        }

    body = json.loads(event['body'])
    comment_id = event['pathParameters'].get('commentId')
    session_id = body.get('sessionId')

    if not comment_id or not session_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing commentId or sessionId'})
        }

    if 'content' not in body:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing content field'})
        }

    if len(body['content']) > 1000:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Comment content too long'})
        }

    try:
        response = comments_table.scan(
            FilterExpression=Attr('commentId').eq(comment_id)
        )

        if not response['Items']:
            return {
                'statusCode': 404,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': 'Comment not found'})
            }

        comment = response['Items'][0]
        if comment['sessionId'] != session_id:
            return {
                'statusCode': 403,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': 'Unauthorized'})
            }

        if comment.get('isDeleted', False):
            return {
                'statusCode': 400,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': 'Cannot update deleted comment'})
            }

        update_response = comments_table.update_item(
            Key={
                'commentId': comment_id,
                'topicId': comment['topicId']
            },
            UpdateExpression='SET content = :content, updatedAt = :updatedAt',
            ExpressionAttributeValues={
                ':content': body['content'],
                ':updatedAt': datetime.now().isoformat()
            },
            ReturnValues='ALL_NEW'
        )

        return {
            'statusCode': 200,
            'headers': cors_headers(origin),
            'body': json.dumps(update_response['Attributes'], cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': str(e)})
        }

def delete_comment(event, context, origin):
    if 'pathParameters' not in event or 'commentId' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing commentId parameter'})
        }

    comment_id = event['pathParameters']['commentId']

    if 'queryStringParameters' not in event or 'sessionId' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': 'Missing sessionId parameter'})
        }

    session_id = event['queryStringParameters']['sessionId']

    try:
        response = comments_table.scan(
            FilterExpression=Attr('commentId').eq(comment_id)
        )

        if not response['Items']:
            return {
                'statusCode': 404,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': 'Comment not found'})
            }

        comment = response['Items'][0]
        if comment['sessionId'] != session_id:
            return {
                'statusCode': 403,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': 'Unauthorized'})
            }

        if comment.get('isDeleted', False):
            return {
                'statusCode': 400,
                'headers': cors_headers(origin),
                'body': json.dumps({'error': 'Comment already deleted'})
            }

        update_response = comments_table.update_item(
            Key={
                'commentId': comment_id,
                'topicId': comment['topicId']
            },
            UpdateExpression='SET isDeleted = :isDeleted, updatedAt = :updatedAt',
            ExpressionAttributeValues={
                ':isDeleted': True,
                ':updatedAt': datetime.now().isoformat()
            },
            ReturnValues='ALL_NEW'
        )

        return {
            'statusCode': 200,
            'headers': cors_headers(origin),
            'body': json.dumps({
                'message': 'Comment deleted successfully',
                'comment': update_response['Attributes']
            }, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(origin),
            'body': json.dumps({'error': str(e)})
        }
