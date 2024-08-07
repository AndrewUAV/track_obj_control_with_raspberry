import time
import RPi.GPIO as GPIO
from settings import PPM_PIN, PPM_PAUSE


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PPM_PIN, GPIO.OUT)


def generator_ppm(ch1=1500, ch2=1500, ch3=1500, ch4=1500):

    channels_values = (ch1, ch2, ch3, ch4)

    GPIO.output(PPM_PIN, GPIO.HIGH)
    # time of start pulse
    time.sleep(0.0003)

    for val in channels_values:
        send_ppm(val)

    # end of ppm pulse
    GPIO.output(PPM_PIN, GPIO.LOW)
    time.sleep(PPM_PAUSE)


def send_ppm(val):

    GPIO.output(PPM_PIN, GPIO.LOW)
    time.sleep(val / 1000000.0)
    GPIO.output(PPM_PIN, GPIO.HIGH)



