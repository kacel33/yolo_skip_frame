import cv2
import time
import numpy as np
from yolo import yolo
from yolo import Parser
import argparse


size_list = [320, 416, 608]
args = Parser()
cap = cv2.VideoCapture(args.video)

YOLO = True
N_num = int(input("determine skip frame:"))


z = N_num
time_ = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    start = time.time()
    if frame is None:
        break

    if z == N_num:
        YOLO = True
        z = 0

    if YOLO is True:
        yolo_frame, boxes, confidence = yolo(frame=frame, size=size_list[2], score_threshold=0.4, nms_threshold=0.4,
                                             gpu=args.gpu)
        cv2.imshow("Frame", yolo_frame)
        # cv2.imwrite('yolo.jpg', yolo_frame)

        YOLO = False
        if N_num ==0:
            YOLO = True
        print('time:', time.time() - start)

    else:
        for box, confi in zip(boxes, confidence):
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255))
            cv2.putText(frame, confi, (x, y - 8), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

        cv2.imshow("Frame", frame)
        print('time:', time.time() - start)

    z = z + 1
    k = cv2.waitKey(1)
    if k == 27: break

print('all time:', time.time() - time_)
cap.release()
cv2.destroyAllWindows()