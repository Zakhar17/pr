import cv2
import numpy as np
from lab_1.lab_1_helpers import *

cam = cv2.VideoCapture(0)
img_counter = 0
RESOLUTION = (640, 480)

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    cv2.imshow("main_frame", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        # Save img to file
        img_name = "..\\storage\\lab_1\\opencv_camshot_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        img_counter += 1
        # Read the saved img and open in a new window
        img = cv2.imread(img_name, 0)
        height, width = img.shape
        line_color, rect_color = rand_tuples(0, 255, 3, 2)
        line_sp, line_ep = rand_2d_point(0, width-1, 0, height-1, 2)
        rect_sp, rect_ep = rand_2d_point(0, width-1, 0, height-1, 2)
        # Convert image to BGR, so that geometrical figures are coloured
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.line(img, line_sp, line_ep, line_color, 10)
        img = cv2.rectangle(img, rect_sp, rect_ep, rect_color, 10)
        cv2.namedWindow(img_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(img_name, img)
    elif k & 0xFF == ord('r'):
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('..\\storage\\lab_1\\output_.avi', fourcc, 20.0, RESOLUTION)
        print('recording video')
        while cam.isOpened():
            ret, frame = cam.read()
            if ret == True:
                # Reset direction, speed, size and color
                frame = cv2.flip(frame, 1)

                out.write(frame)

                cv2.imshow('main_frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        print('video recorded')
        # Init variables for Audi logo motion
        i = 0
        next_point = np.array(rand_2d_point(0, RESOLUTION[0] - 1, 0, RESOLUTION[1] - 1))
        next_radius = random.randint(15, 45)
        next_color = np.random.randint(0, 255, 3)
        motion_step = random.randint(150, 250)
        shift = np.array([[-1.5, 0], [1.5, 0], [3, 0]])
        cap = cv2.VideoCapture('..\\storage\\lab_1\\output_.avi')
        print('showing recorded video')
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                # Reset direction, speed, size and color
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                if i % motion_step == 0:
                    prev_color, next_color = next_color, np.random.randint(0, 255, 3)
                    prev_radius, next_radius = next_radius, random.randint(15, 200)
                    prev_point, next_point = next_point, np.array(rand_2d_point(0, RESOLUTION[0] - 1, 0, RESOLUTION[1] - 1))
                    motion_step = random.randint(100, 250)

                    delta_point = (next_point - prev_point) / motion_step
                    delta_radius = (next_radius - prev_radius) / motion_step
                    delta_color = (next_color - prev_color) / motion_step
                    i = 0

                n = i % motion_step
                new_point = (prev_point + n*delta_point)
                new_radius = int(prev_radius + n*delta_radius)
                new_color = tuple(((prev_color + n*next_color) % 256).astype(int).tolist())
                # Draw Audi circles
                frame = cv2.circle(frame, tuple(new_point.astype(int).tolist()), new_radius, new_color, 10)
                frame = cv2.circle(frame, tuple((new_point + shift[0]*new_radius).astype(int).tolist()), new_radius, new_color, 10)
                frame = cv2.circle(frame, tuple((new_point + shift[1]*new_radius).astype(int).tolist()), new_radius, new_color, 10)
                frame = cv2.circle(frame, tuple((new_point + shift[2]*new_radius).astype(int).tolist()), new_radius, new_color, 10)
                i += 1

                cv2.imshow('recorded_video_frame', frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        out.release()
        print('video record finished')

cam.release()
cv2.destroyAllWindows()