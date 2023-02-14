import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from time import  sleep
detector = HandDetector(detectionCon=0.5, maxHands=1)
cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(3, 1280)
keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
       'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
       'X', 'C', 'V', 'B', 'N', 'M','<', '>', '/', ':']

class Button:
    def __init__(self, pos, text, size=[45, 45]):
        self.pos = pos
        self.size = size
        self.text = text
        #print(self.pos, self.text, self.size[0]+self.pos[0], self.size[1]+self.pos[1])
i = 0
j = 1
button_list = []
for key in keys:
    button = Button((55*i, 55 *j), text=key )
    if i ==20 or i == 10:
        j = j+1
        i   = 0
    else:
        i = i + 1
    button_list.append(button)
final_text = ""
def draw_button(image, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv.rectangle(image, (x, y), (x+w, y+h), (255, 0, 255), cv.FILLED)

        cv.putText(image, button.text, (x+10, y+40), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    return image
while True:
    success, image = cap.read()
    image = detector.findHands(image)
    lmlist, bboxinfo = detector.findPosition(image)
    image = draw_button(image, button_list)

    if lmlist:
        for button in button_list:
            x, y = button.pos
            w, h = button.size

            if x<lmlist[8][0]<x+w and y<lmlist[8][1]<y+w:
                cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), cv.FILLED)

                cv.putText(image, button.text, (x + 10, y + 40), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                l, _, _ = detector.findDistance(8, 12, image)
                if l < 15:
                    final_text+=button.text
                    if button.text == '<':
                        final_text-= button.text
                    sleep(2)
    cv.rectangle(image, (10, 300), (500, 400), (255, 255, 255), cv.FILLED)

    cv.putText(image, final_text, (30, 350), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)



    cv.imshow('image', image)
    cv.waitKey(1)