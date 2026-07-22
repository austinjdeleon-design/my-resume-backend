import json
import os
import boto3

# Initialize the DynamoDB resource and get the table name from environment variables
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Atomically increment the visitor count in DynamoDB (creates item if it doesn't exist)
        response = table.update_item(
            Key={'id': 'visitor-count'},
            UpdateExpression='ADD #count :inc',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        
        current_count = int(response['Attributes']['count'])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({
                'count': current_count
            })
        }
    except Exception as e:
        print(f"Error updating visitor count: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }