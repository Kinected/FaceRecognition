import cv2


def frame_preprocessing(frame, resize_to=None, resolution=None, flip=False):
    if resize_to is not None:
        frame_height, frame_width = frame.shape[:2]

        offset_x = int((frame_width - resize_to[0]) / 2)
        offset_y = int((frame_height - resize_to[1]) / 2)

        frame = frame[offset_y:offset_y + resize_to[1], offset_x:offset_x + resize_to[0]]

    if resolution is not None:
        frame = cv2.resize(frame, resolution)

    if flip:
        frame = cv2.flip(frame, 1)

    return frame
