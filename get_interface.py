"""
This script for create interface of proj
"""
import cv2
from settings import PITCH_MAX, PITCH_MIN, YAW_MAX, YAW_MIN
from convert_angle_to_pulse_signal import func_convert_pitch, func_convert_roll, func_convert_yaw


def draw_interface(image):
    """
    this function for create interface of program
    :param image: frame from video link
    :return: image , center_x, center_y
    center_x and center_y are coords of center image
    """
    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
    dash_length, gap_length = 10, 5

    # horizontal line
    for x in range(0, image.shape[1], dash_length + gap_length):
        cv2.line(image, (x, center_y), (x + dash_length, center_y), (38, 191, 61), thickness=2)

    # vertical line
    for y in range(0, image.shape[0], dash_length + gap_length):
        cv2.line(image, (center_x, y), (center_x, y + dash_length), (38, 191, 61), thickness=2)

    # draw cross
    size = min(image.shape[0], image.shape[1]) // 65
    cv2.line(image, (center_x, center_y - size), (center_x, center_y + size), (32, 35, 181), thickness=2)
    cv2.line(image, (center_x - size, center_y), (center_x + size, center_y), (32, 35, 181), thickness=2)

    # draw rectangle
    rect_width, rect_height = image.shape[1] // 4, image.shape[0] // 4
    top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
    bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)
    cv2.rectangle(image, top_left, bottom_right, (38, 191, 61), thickness=2)

    # draw name system
    text_top = 'Harpy Army Multi Aim System'
    text_bottom = 'Made in UA'
    org_top = (10, image.shape[0] - 30)
    org_bottom = (10, image.shape[0] - 10)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.5
    font_thickness = 1
    color = (0, 255, 0)

    # draw top text
    cv2.putText(image, text_top, org_top, font, font_scale, color, font_thickness, cv2.LINE_AA)
    # draw bottom text
    cv2.putText(image, text_bottom, org_bottom, font, font_scale, color, font_thickness, cv2.LINE_AA)

    # draw flag
    flag_width = 15
    flag_height = 6
    stripe_color1 = (0, 255, 255)
    stripe_color2 = (255, 0, 0)
    flag_bottom_right = (image.shape[1] - 10, image.shape[0] - 10)
    flag_top_left1 = (flag_bottom_right[0] - flag_width, flag_bottom_right[1] - flag_height)
    flag_top_left2 = (flag_bottom_right[0] - flag_width, flag_bottom_right[1] - 2 * flag_height)
    cv2.rectangle(image, flag_top_left1, flag_bottom_right, stripe_color1, -1)
    cv2.rectangle(image, flag_top_left2, (flag_bottom_right[0], flag_bottom_right[1] - flag_height), stripe_color2, -1)

    return image, center_x, center_y


def draw_angle(image, pitch=0.0, yaw=0.0, roll=0.0):
    """
    This function for get angle from image for generate control signal and visualization on frame of video
    :param image: frame from video link
    :param pitch: calculate pitch angle from image
    :param yaw: calculate yaw angle from image
    :param roll: calculate roll angle from accel
    :return: image, pitch, yaw, roll
    """
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 0.5
    font_thickness = 1
    color = (0, 255, 0)

    # draw roll angle
    text_top = f"Roll: {roll:.2f}"
    org_top_angle = (10, 30)
    cv2.putText(image, text_top, org_top_angle, font, font_scale, color, font_thickness, cv2.LINE_AA)

    # draw pitch angle
    text_middle = f"Pitch: {pitch:.2f}"
    org_middle_angle = (10, 60)
    cv2.putText(image, text_middle, org_middle_angle, font, font_scale, color, font_thickness, cv2.LINE_AA)

    # draw yaw angle
    text_bottom = f"Yaw: {yaw:.2f}"
    org_bottom_angle = (10, 90)
    cv2.putText(image, text_bottom, org_bottom_angle, font, font_scale, color, font_thickness, cv2.LINE_AA)
    return image, pitch, yaw, roll


def draw_pulse_of_channels(image, pitch=0.0, yaw=0.0, roll=0.0):
    """
    This function for draw value on rc control channels
    :param image: frame from video link
    :param pitch: calculate pitch angle from image
    :param yaw: calculate yaw angle from image
    :param roll: calculate roll angle from accel
    :return: image
    """
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 0.5
    font_thickness = 1
    color = (128, 0, 0)

    # get pulse of channels
    CH2 = func_convert_roll(roll)
    CH3 = func_convert_pitch(pitch)
    CH5 = func_convert_yaw(yaw)

    # draw channel of roll
    text_ch_rll = f'CH2: {CH2:}'
    org_ch_rll = (150, 30)
    cv2.putText(image, text_ch_rll, org_ch_rll, font, font_scale, color, font_thickness, cv2.LINE_AA)

    # draw channel of pitch
    text_ch_ptch = f'CH3: {CH3:}'
    org_ch_ptch = (150, 60)
    cv2.putText(image, text_ch_ptch, org_ch_ptch, font, font_scale, color, font_thickness, cv2.LINE_AA)

    # draw channel of yaw
    text_ch_yaw = f'CH5: {CH5:}'
    org_ch_yaw = (150, 90)
    cv2.putText(image, text_ch_yaw, org_ch_yaw, font, font_scale, color, font_thickness, cv2.LINE_AA)

    return image


def draw_line_tracker(image, x1, y1, x2, y2):
    """
    This function for create line traker from center of image to center of aim
    :param image: frame from video link
    :param x1: center_x of image
    :param y1: center_y of image
    :param x2: center_x of aim
    :param y2: center_y of aim
    :return:
    """
    cv2.line(image, (x1, y1), (x2, y2),(32, 35, 181), thickness=2)
    return image


def get_angle_aim_from_image(image, center_aim_x=0.0, center_aim_y=0.0):
    height, wight = image.shape[0], image.shape[1]

    # calculate pitch angle
    pitch_up, pitch_down = PITCH_MAX, PITCH_MIN
    pitch_difference = pitch_up - pitch_down
    pitch_angle_per_pixel = pitch_difference / height
    pitch = pitch_up - center_aim_y*pitch_angle_per_pixel

    # calculate yaw angle
    yaw_left, yaw_right = YAW_MIN, YAW_MAX
    yaw_difference = yaw_right - yaw_left
    yaw_angle_per_pixel = yaw_difference / wight
    yaw = yaw_left + center_aim_x*yaw_angle_per_pixel
    return pitch, yaw


def get_aim(image, bboxs):
    center_x_aim = image.shape[1] // 2
    center_y_aim = image.shape[0] // 2

    if bboxs is not None and len(bboxs) > 0:
        for bbox in bboxs:
            left, top, width, height = bbox['bbox']

            center_x_aim = left + width // 2
            center_y_aim = top + height // 2

            #radius1 = min(width, height) // 4
            #radius2 = min(width, height) // 60
            radius1 = 45
            radius2 = 1
            #cv2.rectangle(image, (left, top), (left + width, top + height), (0, 0, 255), 2)

            # draw circle 1
            cv2.circle(image, (center_x_aim, center_y_aim), radius1, (32, 35, 181), thickness=2)
            # draw circle 2
            cv2.circle(image, (center_x_aim, center_y_aim), radius2, (32, 35, 181), thickness=7)

            cv2.putText(image, "Aim", (left + 20, top + 50), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (32, 35, 181), 2)

            # is aim
            cv2.putText(image, "Aim detected", (image.shape[1] - 350, image.shape[0] - 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (38, 191, 61), 2)
    else:

        cv2.putText(image, "No aim", (image.shape[1] - 250, image.shape[0] - 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (32, 35, 181), 2)

    return image, center_x_aim, center_y_aim

