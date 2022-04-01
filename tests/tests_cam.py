import cv2
import numpy as np
import math
from CV2_Personnal_Utils import assemble_frames


def extract_matrix(frame, center_x, center_y, size):
    w, h = frame.shape
    x_start = max(center_x - size, 0)
    y_start = max(center_y - size, 0)

    x_end = min(center_x + size, w)
    y_end = min(center_y + size, h)

    return np.array(frame[x_start: x_end, y_start: y_end])


def apply_houghP(source, display=None, shift=None):
    if display is None:
        display = source
    if shift is None:
        shift = (0, 0)
    ret, bin_img = cv2.threshold(source, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(bin_img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 70, minLineLength=10, maxLineGap=250)

    if lines is None:
        return edges, bin_img

    for line in lines:
        x1, y1, x2, y2 = line[0]
        x1 += shift[0]
        x2 += shift[0]
        y1 += shift[1]
        y2 += shift[1]
        cv2.line(display, (x1, y1), (x2, y2), 255, 2)
        cv2.circle(display, (x1, y1), 4, 255, 5)
        cv2.circle(display, (x2, y2), 4, 255, 5)

    return edges, bin_img


def apply_hough(source, display=None, shift=None):
    if display is None:
        display = source
    if shift is None:
        shift = (0, 0)
    ret, bin_img = cv2.threshold(source, 50, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(bin_img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)

    if lines is None:
        return edges, bin_img

    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho + shift[0]
        y0 = b * rho + shift[1]
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv2.line(display, pt1, pt2, 255, 2)

    return edges, bin_img


if __name__ == "__main__":

    cam = cv2.VideoCapture(2)

    while True:
        ret, frame = cam.read()

        # working_frame = frame[:, 270:490]
        frame = frame[:1280, :720]
        working_frame = np.copy(frame)
        working_frame = cv2.cvtColor(working_frame, cv2.COLOR_BGR2GRAY)

        working_frame = extract_matrix(working_frame, working_frame.shape[0]//2, working_frame.shape[1]//2, 100)

        hough = np.copy(frame)
        houghP = np.copy(frame)
        apply_hough(working_frame, hough, (220, 135))
        apply_houghP(working_frame, houghP, (220, 135))

        raw_hough = np.copy(working_frame)
        raw_houghP = np.copy(working_frame)

        edges1, edges2, bin1, bin2 = None, None, None, None
        res1 = apply_hough(raw_hough)
        if res1 is not None:
            edges1, bin1 = res1

        res2 = apply_houghP(raw_houghP)
        if res2 is not None:
            edges2, bin2 = res2

        bin_data = cv2.threshold(working_frame, 50, 255, cv2.THRESH_BINARY_INV)[1]

        display = assemble_frames(hough, houghP)
        display = assemble_frames(display, cv2.cvtColor(raw_hough, cv2.COLOR_GRAY2RGB), 50, 0)
        display = assemble_frames(display, cv2.cvtColor(raw_houghP, cv2.COLOR_GRAY2RGB), 700, 0)
        if edges1 is not None:
            display = assemble_frames(display, cv2.cvtColor(edges1, cv2.COLOR_GRAY2RGB), 50, 200)
        if bin1 is not None:
            display = assemble_frames(display, cv2.cvtColor(bin1, cv2.COLOR_GRAY2RGB), 50, 400)
        if edges2 is not None:
            display = assemble_frames(display, cv2.cvtColor(edges2, cv2.COLOR_GRAY2RGB), 700, 200)
        if bin2 is not None:
            display = assemble_frames(display, cv2.cvtColor(bin2, cv2.COLOR_GRAY2RGB), 700, 400)

        cv2.imshow('frame', display)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
