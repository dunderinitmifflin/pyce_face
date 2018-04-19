from __future__ import print_function
import boto3
from botocore.vendored import requests
import json


rekognition = boto3.client('rekognition', region_name='us-west-2')
dynamodb = boto3.client('dynamodb', region_name='us-west-2')
iot = boto3.client('iot-data', region_name='us-west-2')


def search_faces(bucket, key, threshold=90):
    """ comapares image against DB """
    message = rekognition.search_faces_by_image(
        Image={"S3Object":
               {"Bucket": bucket,
                "Name": key}},
        CollectionId="base_line_photos",
        FaceMatchThreshold=threshold,)
    return message


def response(message, status_code):
    """ returns confirmation"""
    return {
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }


def lambda_handler(event, context):
    """ preps message for API """
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        message = search_faces(bucket, key)
        for match in message['FaceMatches']:
            answer = match['Face']['FaceId']
            answer = response({'rekognitionId': answer}, 202)
            return answer

    except Exception as e:
        return e
