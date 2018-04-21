import boto3
import io
from PIL import Image
from send_pic_to_register import get_files, remove_local
from send_pic_to_register import query_mysql_db_for_rek_id

rekognition = boto3.client(
    'rekognition',
    aws_access_key_id = 'AKIAJ7YQ463O62CNGIMQ',
    aws_secret_access_key = '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',
    region_name = 'us-west-2')
dynamodb = boto3.client('dynamodb',
    aws_access_key_id = 'AKIAJ7YQ463O62CNGIMQ',
    aws_secret_access_key = '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',
    region_name = 'us-west-2')
directory = '/home/pi/camera/'



##pic_path = '/home/pi/camera/image_1523923459.4097712.jpg'




def search_faces():
    list_of_jpgs = get_files(directory)
    pic_path = '{}{}'.format(directory, list_of_jpgs[0])

    image = Image.open(pic_path)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()
    
    message = rekognition.search_faces_by_image(
        Image={'Bytes':image_binary},
        CollectionId='pyface_demos',
        FaceMatchThreshold = 90)
    
    remove_local(pic_path)
##    print (message['FaceMatches'])
    for match in message['FaceMatches']:
        result = query_mysql_db_for_rek_id(match['Face']['FaceId'])
        if result is not None:
##        print('FaceId')
##        print(match['Face']['FaceId'])
##        print (match['Face']['FaceId'],match['Face']['Confidence'])
            return (match['Face']['FaceId'])


##search_faces()
