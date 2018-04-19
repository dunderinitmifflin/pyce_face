from __future__ import print_function

import boto3
from decimal import Decimal
import json
import uuid
import urllib

print('Loading function')

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

""" Note: you have to create the collection first!
 rekognition.create_collection(CollectionId='base_line_photos')
 --------------- Helper Functions ------------------ """


def index_faces(bucket, key):
    """ grabs image form bucket """
    response = rekognition.index_faces(
        Image={"S3Object":
               {"Bucket": bucket,
                "Name": key}},
        CollectionId="base_line_photos")
    return response


def update_index(fileName, tableName, sfaceId):
    """ adds image to db """
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'ImageId': {'S': fileName},
            }
        ) 
    
# --------------- Main handler ------------------


def lambda_handler(event, context):

    """ Get the object from the event"""
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:

        """ Calls Amazon Rekognition IndexFaces API to detect faces in S3 object
        to index faces into specified collection """

        response = index_faces(bucket, key)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            ret = s3.head_object(Bucket=bucket, Key=key)

            update_index(key, 'base_line_photos', faceId)

        """ Print response to console """
        print(response)

        return response['FaceRecords'][0]['Face']['FaceId']
  
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. "
              .format(key, bucket))
        raise e
