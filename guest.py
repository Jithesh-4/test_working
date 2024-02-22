import firebase_admin
import RPi.GPIO as GPIO
import time
import cv2
import random
from firebase_admin import credentials, db
from threading import Thread

# Replace with your Firebase project credentials
cred = credentials.Certificate("/home/pi/Desktop/pmain/predictive-maintainence-1841d-firebase-adminsdk-oejc1-37178fae8b.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://predictive-maintainence-1841d-default-rtdb.firebaseio.com/'})

# Define the path in the Firebase Realtime Database
belt = '/BELT POSITION'
current = '/CURRENT'
position = '/POSITION'
rpm = '/RPM'
sound = '/SOUND DECIBEL'
temp = '/TEMPERATURE'
vis = '/OIL VISCOSITY'
volt = '/VOLTAGE'
motor = '/MOTOR TEMPERATURE'


display_width = 2020  # Set the desired width
display_height = 1000  # Set the desired height

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2020)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

def cameraOpenCam():
	while True:
		(ret, frame) = cap.read() 
		count = 0
		sensor1_value = 0
		sensor2_value = 0
		sensor3_value = 0
		sensor4_value = 0
		sensor5_value = 0
		sensor6_value = 0
		sensor7_value = 0
		sensor8_value = 0
		sensor9_value = 0
		 

		if not ret:
			print("Error: Could not read a frame.")
			break
    
		if count == 15:
			# Get data from Firebase
			data0 = db.reference(belt).get()
			data1 = 2.5 #db.reference(current).get()
			data2 = db.reference(position).get()
			data3 = db.reference(rpm).get()
			data4 = db.reference(sound).get()
			data5 = db.reference(temp).get()
			data6 = db.reference(vis).get()
			data7 = db.reference(volt).get()
			data8 = db.reference(motor).get()
			if data0 is not None:
				# Process the received data
				print("Belt:", data0)
				print("Current:", data1)
				print("Position:", data2)
				print("RPM:", data3)
				print("Sound Decibel:", data4)
				print("Temperature:", data5)
				print("Viscosity:", data6)
				print("Voltage:", data7)
				print("Motor Temperature:", data8)
				# Add your logic here to perform actions based on the received data
				# For example, you can control GPIO pins, sensors, actuators, etc.
    
			# Generate random values for each sensor
			sensor1_value = data0
			sensor2_value = data1
			sensor3_value = data2
			sensor4_value = data3
			sensor5_value = data4
			sensor6_value = data5
			sensor7_value = data6
			sensor8_value = data7
			sensor9_value = data8

			count = 0
		# Draw rectangles and labels for each sensor
		cv2.rectangle(frame, (1100, 290), (1250, 390), (255, 0, 0), 2)
		cv2.putText(frame, f"Belt: {sensor1_value}", (1100, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

		cv2.rectangle(frame, (900, 590), (1050, 690), (0, 255, 255), 2)
		cv2.putText(frame, f"Current: {sensor2_value}", (900, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
	
		cv2.rectangle(frame, (700, 440), (850, 540), (255, 255, 0), 2)
		cv2.putText(frame, f"Position: {sensor3_value}", (700, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

		cv2.rectangle(frame, (1100, 590), (1250, 690), (0, 255, 255), 2)
		cv2.putText(frame, f"RPM: {sensor4_value}", (1100, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

		cv2.rectangle(frame, (450, 50), (600, 150), (0, 0, 255), 2)
		cv2.putText(frame, f"dB Level: {sensor5_value}", (450, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
		cv2.rectangle(frame, (650, 50), (800, 150), (0, 0, 255), 2)
		cv2.putText(frame, f"Temperature: {sensor6_value}", (650, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
		cv2.rectangle(frame, (220, 420), (370, 520), (255, 0, 0), 2)
		cv2.putText(frame, f"Viscosity: {sensor7_value}", (220, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    
		cv2.rectangle(frame, (700, 590), (850, 690), (0, 255, 255), 2)
		cv2.putText(frame, f"Voltage: {sensor8_value}", (700, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
		cv2.rectangle(frame, (900, 400), (1050, 500), (255, 255, 0), 2)
		cv2.putText(frame, f"Cooler: {sensor9_value}", (900, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    
		# Resize the frame to the desired display size
		frame = cv2.resize(frame, (display_width, display_height))

		cv2.imshow('Webcam', frame)
		count = count + 1

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break    

if __name__ == '__main__':
	Thread(target=cameraOpenCam).start()
