
import cv2
import convert_angle_to_pulse_signal as get_pulse
from generate_ppm import generate_ppm
from cvzone.FaceDetectionModule import FaceDetector
from get_interface import get_angle_aim_from_image, draw_line_tracker
from get_interface import draw_interface, draw_angle, draw_pulse_of_channels, get_aim


def main():

    cap = cv2.VideoCapture(0)
    ws, hs = 1280, 720
    cap.set(3, ws)
    cap.set(4, hs)

    detector = FaceDetector()

    # the main cycle
    while cap.isOpened():
        success, img = cap.read()

        img, bboxs = detector.findFaces(img, draw=False)

        # get circles of aim and coords of center aim
        aim, center_aim_x, center_aim_y = get_aim(img, bboxs)

        pitch, yaw = get_angle_aim_from_image(img, center_aim_x, center_aim_y)
        roll = yaw * 0.2 # 20% of yaw angle

        # get interface of system and coords of center image
        frame_with_interface, center_img_x, center_img_y = draw_interface(img)

        # draw pitch, yaw and roll angle on image
        draw_angle(img, pitch, yaw, roll)

        # draw value of channels
        draw_pulse_of_channels(img, pitch, yaw, roll)

        # draw line traker
        draw_line_tracker(img, center_img_x, center_img_y, center_aim_x, center_aim_y)

        # draw interface
        cv2.imshow('Harpy Aim System', frame_with_interface)

        ch1 = 1500
        ch2 = get_pulse.func_convert_roll(roll)
        ch3 = get_pulse.func_convert_pitch(pitch)
        ch4 = 1500
        ch5 = get_pulse.func_convert_yaw(yaw)
        ch6 = 1500

        # generate control signal for flight controller
        #generate_ppm(ch1, ch2, ch3, ch4, ch5, ch6)

        print(f'CH1 - {ch1} | CH2 - {ch2} |CH3 - {ch3} |CH4- {ch4} |CH5 - {ch5} |CH6 - {ch6} ')

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
