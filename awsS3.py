#sends and receives data to S3

#!/usr/bin/python
# import RPi.GPIO as IO 
import boto3
import json
import time 
from sense_hat import SenseHat
import sys
import serial
import io


def temp_and_humidity():
    sense = SenseHat()
    sense.clear()
    
    temp = sense.get_temperature()
    temp = 1.8 * round(temp, 1)  + 32 

    humidity = sense.get_humidity()

    pressure = sense.get_pressure()

    return (temp, humidity, pressure)

def serialFunction(duration):
	ser = serial.Serial('/dev/ttyACM0')
	print(ser.name)
	ser.baudrate = 9600 
	ser.timeout = 1
	print("Port open: " + str(ser.is_open))

	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
	ser.reset_input_buffer()
	sio.write(str(duration*1000) + "\n")
	sio.flush()
	
	while ser.inWaiting() == 0:
		print("Waiting for data....")
		time.sleep(.5)
	print("bytes: " + str(ser.inWaiting()))
	dataIn = sio.read()
	print(dataIn)
	return dataIn


while True:
	print("getting s3 object...")
	s3 = boto3.resource('s3')
	content_object = s3.Object('iotwateringproject', 'general_key')

	print("reading json...")
	file_content = content_object.get()['Body'].read().decode('utf-8')
	json_content = json.loads(file_content)

	print("parsing instructions...")
	duration = int(json_content["frontend"]["duration"])
	willWater = json_content["frontend"]["willWater"]
	print("willWater = ",str(willWater))
	print("duration = ", str(duration))

	waterDetected = "5555"

	if willWater == "True":
		print("starting servo for duration...")
		waterDetected = serialFunction(int(duration))
		print("stopping servo...")

    
	    #check is water detected

	json_content["data"]["isWaterDetected"] = str(waterDetected)
		
	sensors = temp_and_humidity()
	json_content["data"]["Temperature"] = str(sensors[0])
	json_content["data"]["Humidity"] = str(sensors[1])
	json_content["data"]["Pressure"] = str(sensors[2])

	print("updating json...")
	with open('example.json', 'w') as f:
		json.dump(json_content, f, ensure_ascii=False)

	print("uploading to s3...")
	s3.Bucket("iotwateringproject").upload_file('example.json', 'general_key')


	print("sleeping for 3600 seconds")
	time.sleep(3600) #time until next run




