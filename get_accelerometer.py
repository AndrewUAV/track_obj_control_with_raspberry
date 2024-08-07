import smbus
import math
import time

DEVICE_ADDRESS = 0x68
MPU6050_RA_ACCEL_XOUT_H = 0x3B
MPU6050_RA_ACCEL_YOUT_H = 0x3D
MPU6050_RA_ACCEL_ZOUT_H = 0x3F
ACCEL_SCALE = 16384.0


def read_word_2c(bus, addr):
    high = bus.read_byte_data(DEVICE_ADDRESS, addr)
    low = bus.read_byte_data(DEVICE_ADDRESS, addr + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

# settings for accelerometer
bus = smbus.SMBus(1)
bus.write_byte_data(DEVICE_ADDRESS, 0x6B, 0x00)  # reset
bus.write_byte_data(DEVICE_ADDRESS, 0x6B, 0x01)  # power on
time.sleep(0.1)

def get_roll(accel_y, accel_z):
    roll = math.atan2(accel_y, accel_z) * (180 / math.pi)
    return roll

def get_pitch(accel_x, accel_y, accel_z):
    pitch = math.atan2(-accel_x, math.sqrt(accel_y * accel_y + accel_z * accel_z)) * (180 / math.pi)
    return pitch

while True:
    accel_x_raw = read_word_2c(bus, MPU6050_RA_ACCEL_XOUT_H)  # Используем bus
    accel_y_raw = read_word_2c(bus, MPU6050_RA_ACCEL_YOUT_H)  # Используем bus
    accel_z_raw = read_word_2c(bus, MPU6050_RA_ACCEL_ZOUT_H)  # Используем bus

    accel_x = accel_x_raw / ACCEL_SCALE
    accel_y = accel_y_raw / ACCEL_SCALE
    accel_z = accel_z_raw / ACCEL_SCALE

    roll = get_roll(accel_y, accel_z)
    pitch = get_pitch(accel_x, accel_y, accel_z)

    print("Roll: {:.2f} degrees".format(roll))
    print("Pitch: {:.2f} degrees".format(pitch))

    time.sleep(0.5)