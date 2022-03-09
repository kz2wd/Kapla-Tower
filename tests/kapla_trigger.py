import time

import cv2
import numpy as np
import math
from CV2_Personnal_Utils import assemble_frames, draw_grid


def extract_matrix(frame, start_x, start_y, size_x, size_y):
    w, h = frame.shape[:2]

    end_x = min(start_x + size_x, w)
    end_y = min(start_y + size_y, h)

    return np.array(frame[start_y: end_y, start_x: end_x])


def apply_houghP(source):
    ret, bin_img = cv2.threshold(source, 150, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(bin_img, 50, 150, apertureSize=3)
    # blur = cv2.GaussianBlur(edges, (3, 3), 0)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, minLineLength=50, maxLineGap=15)

    return lines, edges


def print_lines(lines, display, color, shift=None):
    if shift is None:
        shift = (0, 0)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = apply_shift(*line[0], shift)
            cv2.line(display, (x1, y1), (x2, y2), color, 2)
            cv2.circle(display, (x1, y1), 4, color, 5)
            cv2.circle(display, (x2, y2), 4, color, 5)


def apply_shift(x1, y1, x2, y2, shift):
    x1 += shift[0]
    x2 += shift[0]
    y1 += shift[1]
    y2 += shift[1]
    return x1, y1, x2, y2



def has_similar(lines, line, epsilon=5):
    for l in lines:
        # print(abs(l[0][0] - line[0][0]), abs(l[0][1] - line[0][1]), abs(l[0][2] - line[0][2]), abs(l[0][3] - line[0][3]))
        if abs(l[0][0] - line[0][0]) < epsilon or abs(l[0][1] - line[0][1]) < epsilon \
                or abs(l[0][2] - line[0][2]) < epsilon or abs(l[0][3] - line[0][3]) < epsilon:
            return True
    return False


def simplify_lines(lines, epsilon=5):
    for i in range(len(lines) - 1, 0, -1):
        if has_similar(lines[:i], lines[i], epsilon):
            lines = np.delete(lines, i, 0)
    return lines


def get_kapla_pos(lines, display, shift=None):
    if shift is None:
        shift = (0, 0)
    lines_distance = {math.sqrt(pow(x[0][2] - x[0][0], 2) + pow(x[0][3] - x[0][1], 2)): x for x in lines}

    dist_max = max(lines_distance)
    longest = lines_distance[dist_max]
    # print(dist_max)
    # print(f"ratio {dist_max / 70} pix/mm")


    x1, y1, x2, y2 = apply_shift(*longest[0], shift)
    cv2.line(display, (x1, y1), (x2, y2), (0, 255, 0), 3)

    average_line = np.mean(lines, 0)
    x1, y1, x2, y2 = apply_shift(*map(int, average_line[0]), shift)
    cv2.line(display, (x1, y1), (x2, y2), (0, 0, 255), 4)







if __name__ == "__main__":

    cam = cv2.VideoCapture(2)

    while True:
        ret, frame = cam.read()

        # working_frame = frame[:, 270:490]
        # frame = frame[:1280, :720]
        working_frame = np.copy(frame)

        # draw_grid(frame, 50, (0, 255, 255))
        # draw_grid(frame, 100, (255, 0, 255))

        working_frame = cv2.cvtColor(working_frame, cv2.COLOR_BGR2GRAY)

        shift = (275, 150)
        # shift = (0, 0)
        working_frame = extract_matrix(working_frame, shift[0], shift[1], 150, 100)
        # working_frame = extract_matrix(working_frame, shift[0], shift[1], 300, 300)

        lines, edges = apply_houghP(working_frame)

        if lines is not None:
            # before_clean = len(lines)
            # print_lines(lines, frame, (75, 75, 75), shift)
            # lines = simplify_lines(lines, 5)
            # print(f"{before_clean} => {len(lines)}")
            print_lines(lines, frame, (250, 0, 0), shift)
            get_kapla_pos(lines, frame, shift)

        else:
            print("No line")

        display = assemble_frames(frame, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))

        cv2.imshow('frame', display)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        time.sleep(1)

    cam.release()
    cv2.destroyAllWindows()
