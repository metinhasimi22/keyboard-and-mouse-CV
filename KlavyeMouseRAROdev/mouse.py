import cv2
import numpy as np
import time
import autopy
from pyautogui import click

import Tracking as ht

class smart_mouse:
    def __init__(self, width=640, height=480, frame_rate=100, smoothening=8):#640 ve 480 olabilir
        # 640 ve 480 olmasının nedeni elini kısa mesafelerde ekranın her yernide götürebilmeni sağlıyor

        self.pTime = 0
        self.width = width # zaten buralar da   görüntünün yükseklik ve genişlik değerleri
        self.height = height
        self.frameR = 100  #kullanıcının elinin ekranın kenarlarına kadar gitmesini engellemek
        self.smoothening = smoothening  #fare hareketinin düzgünleştirilmesi için kullanılan bir parametre
        self.prev_x, self.prev_y = 0, 0  # bu aşağdakilerde FARE KONUMUNU TEMSİL EDER .
        self.curr_x, self.curr_y = 0, 0

        self.cap = cv2.VideoCapture(0)  # buras  zaten video karesini alıyor
        self.cap.set(3, width)
        self.cap.set(4, height)

        self.detector = ht.handDetector(maxHands=1)  # bizim el dedektörü
        self.screen_width, self.screen_height = autopy.screen.size()

    def run(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)  # Görüntüyü yatay eksende ters çevir
            img = self.detector.findHands(img)
            lmlist, bbox = self.detector.findPosition(img)

            if len(lmlist)!=0:# El pozisyonlarının tespit edildiğinden emin olmak için el pozisyonu listesinin boş olup olmadığını kontrol et.
    # Parmak uçlarının koordinatlarını al
                # parmak rotasyonları
                x1, y1 = lmlist[8][1:] # İşaret parmağının uç noktasının (8. eklem) x ve y koordinatları
                x2, y2 = lmlist[12][1:]# Orta parmağın uç noktasının (12. eklem) x ve y koordinatları


                fingers = self.detector.fingersUp()  # Hangi parmakların yukarıda olduğunu kontrol et (1=yukarıda, 0=aşağıda).

                cv2.rectangle(img, (self.frameR, self.frameR), (self.width - self.frameR, self.height - self.frameR), (255, 0, 255), 2)
                if fingers[1] == 1 and fingers[2] == 0:
                    x3 = np.interp(x1, (self.frameR, self.width - self.frameR), (0, self.screen_width))
                    y3 = np.interp(y1, (self.frameR, self.height - self.frameR), (0, self.screen_height))

                    self.curr_x = self.prev_x + (x3 - self.prev_x) / self.smoothening
                    self.curr_y = self.prev_y + (y3 - self.prev_y) / self.smoothening

                    autopy.mouse.move(self.curr_x, self.curr_y)
                    cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                    self.prev_x, self.prev_y = self.curr_x, self.curr_y


                if fingers[1] == 1 and fingers[2] == 1:
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)
                    # değerler yan yana gelince yapılması gereken click işlemi
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        click()
                        #autopy.mouse.click()

                        continue

            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)

            # Klavyeden 'q' tuşuna basıldığında çık
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
def click():
    autopy.mouse.click()

if __name__ == "__main__":
    tracker = smart_mouse()
    tracker.run()

