import subprocess
#import Pi GPIO library button class
from gpiozero import Button, LED, PWMLED
from time import sleep
from lobe import ImageModel
from distance_detection import *
GPIO.setwarnings(False)
import RPi.GPIO as GPIO
import time
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()




#---------SERVO_IMPORTS-------------------------#
import time

from board import SCL, SDA
import busio
from trash_classifier import *
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_pca9685 import PCA9685

from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 50

#-------------------------------------------------#

# Load Lobe TF model
# --> Change model file path as needed
model = ImageModel.load('/home/pi/Lobe/model')

# Take Photo
def take_photo():
    return_code = subprocess.call("./webcam.sh")
    print("Picture taken!!!!!!")


#------------------SERVO CODE_ INTEGRATION-----------#
def platform_servo_ON():
    kit.servo[1].angle = 0


def platform_servo_OFF():
    kit.servo[1].angle = 180



def PAPER_fun():
    print("MOVE TOWARDS PAPER BIN \n")
    kit.servo[2].angle = 180
    time.sleep(5)


def PLASTIC_fun():
    print("MOVE TOWARDS PLASTIC BIN \n")
    kit.servo[2].angle = 140
    time.sleep(5)


def METAL_fun():
    print("MOVE TOWARDS METAL BIN \n")
    kit.servo[2].angle = 100
    time.sleep(5)


def ORGANIC_fun():
    print("MOVE TOWARDS ORGANIC BIN \n")
    kit.servo[2].angle = 60
    time.sleep(5)


def DEFAULT_POS_fun():
    print("MOVE TOWARDS DEFAULT BIN POSITION \n")
    kit.servo[2].angle = 20
    time.sleep(5)

#-----------------------------------------------------------------------#
# Identify prediction and turn on appropriate LED
def led_select(label):
    print(label)
    if  label == "paper":
        PAPER_fun()
        platform_servo_ON()
        print("Paper waste")
        sleep(5)
        platform_servo_OFF()
        sleep(0.5)
        DEFAULT_POS_fun()

    if  label == "plastic":
        PLASTIC_fun()
        platform_servo_ON()
        print("Plastic waste")
        sleep(5)
        platform_servo_OFF()
        sleep(0.5)
        DEFAULT_POS_fun()

    if  label == "metal":
        METAL_fun()
        platform_servo_ON()
        print("Metal waste")
        sleep(5)
        platform_servo_OFF()
        sleep(0.5)
        DEFAULT_POS_fun()

    if  label == "organic":
        METAL_fun()
        platform_servo_ON()
        print("Organic waste")
        sleep(5)
        platform_servo_OFF()
        sleep(0.5)
        DEFAULT_POS_fun()
        
    if result == "not trash!":
        DEFAULT_POS_fun()
        sleep(5)

    else:
        print ("System is off!!!!!!!!!!!!!")

    time.sleep(5)
#-----------------------------------------------------------------------#
# Main Function
while True:
    print("Hold a tag near the reader")
    id, text = reader.read()
    
#     print("ID: %s\nText: %s" % (id,text))

    
    time.sleep(2)
    if id == 290251161272:
     print("id %s is a verified user" % (id))
 


    # calling functions
     distance()
     dist = distance()
    #print("Measured Distance = %.1f cm" % dist)
    
     if  dist<=17:
        take_photo()
        # Run photo through Lobe TF model
        result = model.predict_from_file('/home/pi/Lobe/webcam/image.jpg')
        # --> Change image path
        led_select(result.prediction)
        time.sleep(2)
        
     else:
         print ("Retake the picture!!!!!!")
     sleep(1)
    else:
       print ("%s you are unverified user" % (id)) 


