"""
This script for convert angle from accel angle to ppm signal
"""
from settings import MAX_PULSE, MIN_PULSE, PITCH_MIN, PITCH_MAX, ROLL_MIN, ROLL_MAX, YAW_MIN, YAW_MAX


def convert_angle_to_mc(min_angle, max_angle, angle):
    """
    :param min_angle: min limit of range angle
    :param max_angle: max limit of range angle
    :param angle: current angle
    :return: pulse_width for control of axis
    """
    if angle > max_angle:
        pulse_width = MIN_PULSE
    elif angle < min_angle:
        pulse_width = MIN_PULSE
    else:
        pulse_width = MIN_PULSE + ((angle - min_angle) / (max_angle - min_angle)) * (MAX_PULSE - MIN_PULSE)
    return int(pulse_width)


def func_convert_throttle_to_mc(sector):

    if sector == 1:
        throttle = 60
    elif sector == 2:
        throttle = 80
    elif sector == 3:
        throttle = 100
    else:
        throttle = 60

    ppm_range = MAX_PULSE - MIN_PULSE
    ppm_value = MIN_PULSE + (throttle / 100) * ppm_range
    return int(ppm_value)


def func_convert_pitch(pitch):
    """
    :param pitch: real pitch angle
    :return: pulse_width for control pitch channel
    """
    return convert_angle_to_mc(PITCH_MIN, PITCH_MAX, pitch)


def func_convert_roll(roll):
    """
    :param roll: real roll angle
    :return: pulse_width for control roll channel
    """
    return convert_angle_to_mc(ROLL_MIN, ROLL_MAX, roll)


def func_convert_yaw(yaw):
    """
    :param yaw: real yaw angle
    :return: pulse_width for control yaw channel
    """
    return convert_angle_to_mc(YAW_MIN, YAW_MAX, yaw)
