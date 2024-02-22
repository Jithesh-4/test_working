import firebase_admin
from firebase_admin import credentials, db
import time
import cv2
import random
import threading

# Replace with your Firebase project credentials
cred = credentials.Certificate("/home/pi/Desktop/pmain/fir-demo-c7e7a-firebase-adminsdk-ettih-bb31e7dd26.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://fir-demo-c7e7a-default-rtdb.firebaseio.com/'})

# Define the path in the Firebase Realtime Database
belt = '/sensor-values/beltPosition'
current = '/sensor-values/current'
position = '/sensor-values/position'
rpm = '/sensor-values/rpm'
sound = '/sensor-values/sound'
temp = '/sensor-values/thermometer'
vis = '/sensor-values/oilViscosity'
volt = '/sensor-values/voltage'
motor = '/sensor-values/motorTemp'

# Initialize variables for sensor values
sensor1_value = 0
sensor2_value = 0
sensor3_value = 0
sensor4_value = 0
sensor5_value = 0
sensor6_value = 0
sensor7_value = 0
sensor8_value = 0
sensor9_value = 0

# Set the desired display width and height
display_width = 2020
display_height = 1000

# Initialize the video capture object (using the camera with index 1)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2020)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
cap.set(cv2.CAP_PROP_FPS, 30)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Define a function to retrieve data from Firebase asynchronously
def retrieve_data():
    global sensor1_value, sensor2_value, sensor3_value, sensor4_value, sensor5_value, sensor6_value, sensor7_value, sensor8_value, sensor9_value
    
    while True:
        # Get data from Firebase
        data0 = db.reference(belt).get()
        data1 = db.reference(current).get()
        data2 = db.reference(position).get()
        data3 = db.reference(rpm).get()
        data4 = db.reference(sound).get()
        data5 = db.reference(temp).get()
        data6 = db.reference(vis).get()
        data7 = db.reference(volt).get()
        data8 = db.reference(motor).get()

        # Update sensor values if data is not None
        if data0 is not None:
            sensor1_value = data0
        if data1 is not None:
            sensor2_value = data1
        if data2 is not None:
            sensor3_value = data2
        if data3 is not None:
            sensor4_value = data3
        if data4 is not None:
            sensor5_value = data4
        if data5 is not None:
            sensor6_value = data5
        if data6 is not None:
            sensor7_value = data6
        if data7 is not None:
            sensor8_value = data7
        if data8 is not None:
            sensor9_value = data8

# Start a thread for data retrieval
data_thread = threading.Thread(target=retrieve_data)
data_thread.start()

# Main camera capture loop
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read a frame.")
        break

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
