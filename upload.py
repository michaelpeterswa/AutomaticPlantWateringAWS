#uploads a file to s3. We use this if we want to update the json file on s3


import boto3
import json

s3 = boto3.resource('s3')
content_object = s3.Object('iotwateringproject', 'general_key')

print("uploading to s3...")
s3.Bucket("iotwateringproject").upload_file('example.json', 'general_key')
