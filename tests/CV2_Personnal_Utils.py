import numpy as np
import cv2
import time


def iter_frame(frame, speed):
    h, w, d = frame.shape
    for x in range(1, h, speed):
        for y in range(1, w, speed):
            yield frame[x, y]


def iter_frame_xyp(frame, speed):
    h, w, d = frame.shape
    for x in range(1, h, speed):
        for y in range(1, w, speed):
            yield x, y, frame[x, y]


def get_time(f):
    def modified(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        took = round(time.time() - start, 2)
        print(f'{f.__name__} Took {took}s')
    return modified


def assemble_frames(frame1, frame2, shift_x=None, shift_y=None, default_color=(0, 0, 0)):

    if shift_x is None or shift_y is None:
        shift_x = frame1.shape[1]
        shift_y = 0
    final_size = (max(frame1.shape[0], frame2.shape[0] + shift_y), max(frame1.shape[1], frame2.shape[1] + shift_x), 3)

    result = np.copy(frame1)
    result = np.resize(result, final_size)
    result[:, :] = default_color
    result[:frame1.shape[0], :frame1.shape[1]] = frame1

    result[shift_y:frame2.shape[0] + shift_y, shift_x:frame2.shape[1] + shift_x] = frame2

    return result


def draw_cross(img, center, length, width, color):
    center = list(map(int, center))
    img[max(center[0] - length, 0): min(center[0] + length, img.shape[0]),
        max(center[1] - width, 0): min(center[1] + width, img.shape[1])] = color
    img[max(center[0] - width, 0): min(center[0] + width, img.shape[0]),
        max(center[1] - length, 0): min(center[1] + length, img.shape[1])] = color


def draw_grid(frame, space, color):
    for x in range(0, frame.shape[0], space):
        for y in range(0, frame.shape[1], space):
            draw_cross(frame, (x, y), 3, 3, color)
