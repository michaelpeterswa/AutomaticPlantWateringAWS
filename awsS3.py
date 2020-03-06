 #!/usr/bin/python
# import RPi.GPIO as IO 
import boto3
import json
import time 


while True:
    print("getting s3 object...")
    s3 = boto3.resource('s3')
    content_object = s3.Object('iotwateringproject', 'general_key')

    print("reading json...")
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
     
    print("parsing instructions...")
    duration = json_content["frontend"]["duration"]
    willWater = json_content["frontend"]["willWater"]
    print("willWater = ", willWater)
    print("duration = ", duration)

    if willWater == "True":
        print("starting servo for duration...")
        #start servo
        time.sleep(int(duration))
        #stopp servo
        print("stopping servo...")

    isWaterDetected = False
    #check is water detected

    if isWaterDetected:
        json_content["data"]["isWaterDetected"] = "True"
        print("water is detected")
    else:
        json_content["data"]["isWaterDetected"] = "False"
        print("water is not detected")

    print("updating json...")
    with open('example.json', 'w') as f:
        json.dump(json_content, f, ensure_ascii=False)

    print("uploading to s3...")
    s3.Bucket("iotwateringproject").upload_file('example.json', 'general_key')


    print("sleeping for 3600 seconds")
    time.sleep(3600)




