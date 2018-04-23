#msql
from __future__ import print_function
import mysql.connector

#camera
from picamera import PiCamera
from time import sleep
import time

#S3
##import RPi.GPIO as GPIO
import sys, os, glob, time
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from urllib.request import urlopen

import json

from gpiozero import Button
import RPi.GPIO as GPIO

camera = PiCamera()


##pin = 7
##GPIO.setmode(GPIO.BCM)
##GPIO.setup(pin, GPIO.OUT)

# must hide these things!~
AWS_ACCESS = ''
AWS_SECRET = ''
API_URL = ''

conn = S3Connection(AWS_ACCESS,AWS_SECRET)
bucket = conn.get_bucket('subject-faces')
directory = '/home/pi/camera/'

pin_green = 13
pin_yellow = 6
pin_red = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_green, GPIO.OUT)
GPIO.setup(pin_yellow, GPIO.OUT)
GPIO.setup(pin_red, GPIO.OUT)


def turn_on_one_led_or_none(pin = None):
    GPIO.output(pin_green, GPIO.LOW)
    GPIO.output(pin_yellow, GPIO.LOW)
    GPIO.output(pin_red, GPIO.LOW)
    if pin is not None:
        GPIO.output(pin, GPIO.HIGH)



#main functions
def take_and_send_pic():
    take_pic()
    send_pic()


def take_pic():
    turn_on_one_led_or_none(pin_yellow)
    print('Picture Taking')
    camera.start_preview(alpha=200)
    sleep(3)
    time_now = time.time()
    file_path = '/home/pi/camera/image_{}.jpg'.format(time_now)
    camera.capture(file_path)
    camera.stop_preview()
    print('Picture Taken and Written to {}'.format(file_path))
    print()


def send_pic():
    """file goes to bucket and runs through rekognition """
    filenames = get_files(directory)
    print(filenames)
    for f in filenames:
        print('Uploading {} to Amazon S3 bucket {}'.format(f, bucket))
        upload_S3(directory, f)
##        removeLocal(directory, f)
    print('image loading finished')
##    rekognition_id = get_rek_id()
##    return rekognition_id


# upload to S3
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()


def get_files(dir):
    return [os.path.basename(x) for x in glob.glob(str(dir) + '*.jpg')]


def upload_S3(dir, f):
    cID = "potential collection id"
    k = Key(bucket)
    print('k: {}'.format(k))
    k.key = f
    print('k.key: {}'.format(k.key))
##    setPinHigh()
    k.set_contents_from_filename(dir + f, cb=percent_cb, num_cb=10)
##    setPinLow()

def remove_local(file_path):
    os.remove(file_path)
    

def get_rek_id():
    data = urlopen(API_URL)
    print(data)
    tree = data.read().decode('utf-8')
    print(type(tree))
    print(tree)
    tree = json.loads(tree)
    print(tree)
    print('line after tree')
    

def insert_new_face_into_db(first_name, last_name, email, rekognition_id):
    """ inserts new person into msql database with their rekognition id """
    cnx = mysql.connector.connect(user='pi', host='localhost', password='', database='users_db_1')
    cursor = cnx.cursor()
    add_user = ("INSERT INTO users_a "
               "(first_name, last_name, email, rekognition_id) "
               "VALUES (%s, %s, %s, %s)")
    data_user = (first_name, last_name, email, rekognition_id)
    cursor.execute(add_user, data_user)
    cnx.commit()
    cursor.close()
    cnx.close()

def query_mysql_db_for_rek_id(rekognition_id):
    """ queries database for a certain rekognition id """
    cnx = mysql.connector.connect(user='pi', host='localhost', password='', database='users_db_1')
    cursor = cnx.cursor()
    query = ('SELECT first_name, last_name, email, rekognition_id FROM users_a WHERE rekognition_id="{}"'.format(rekognition_id))
##    print(query)
    cursor.execute(query, rekognition_id)
    result = cursor.fetchone()
##    print('result')
##    print(result)
    cursor.close()
    cnx.close()
    return (result)




