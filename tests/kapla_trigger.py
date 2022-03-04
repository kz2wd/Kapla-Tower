import cv2
import numpy as np
import math
from CV2_Personnal_Utils import assemble_frames


def extract_matrix(frame, start_x, start_y, size_x, size_y):
    w, h = frame.shape

    end_x = min(start_x + size_x, w)
    end_y = min(start_y + size_y, h)

    return np.array(frame[start_y: end_y, start_x: end_x])


def apply_houghP(source, display=None, shift=None):
    if display is None:
        display = source
    if shift is None:
        shift = (0, 0)
    ret, bin_img = cv2.threshold(source, 150, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(bin_img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 70, minLineLength=20, maxLineGap=15)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x1 += shift[0]
            x2 += shift[0]
            y1 += shift[1]
            y2 += shift[1]
            cv2.line(display, (x1, y1), (x2, y2), 255, 2)
            cv2.circle(display, (x1, y1), 4, 255, 5)
            cv2.circle(display, (x2, y2), 4, 255, 5)

    return lines, edges


def get_kapla_pos(lines):
    print(lines[0])
    longest = max(map(lambda x: math.sqrt(pow(x[0][2] - x[0][1], 2) + pow(x[0][3] - x[0][1], 2)), lines))
    print(longest)


if __name__ == "__main__":

    cam = cv2.VideoCapture(2)

    while True:
        ret, frame = cam.read()

        # working_frame = frame[:, 270:490]
        frame = frame[:1280, :720]
        working_frame = np.copy(frame)

        working_frame = cv2.cvtColor(working_frame, cv2.COLOR_BGR2GRAY)

        # working_frame = extract_matrix(working_frame, 200, 200, 100, 100)

        lines, edges = apply_houghP(working_frame, frame, (0, 0))

        if lines is not None:
            get_kapla_pos(lines)

        display = assemble_frames(frame, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))

        cv2.imshow('frame', display)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
