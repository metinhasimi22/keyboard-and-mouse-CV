import time
import sys
import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import os

from mouse import  smart_mouse as mouse

class EllerleKlavye:
    def __init__(self):
        self.Webcam = cv2.VideoCapture(0)
        self.Webcam.set(3, 1280)
        self.Webcam.set(4, 720)
        self.el = mp.solutions.hands
        self.el_ciz = mp.solutions.drawing_utils
        self.klavye = {
            "Q": [(30, 40), (100, 110)],
            "W": [(120, 40), (180, 110)],
            "E": [(200, 40), (260, 110)],
            "R": [(280, 40), (340, 110)],
            "T": [(360, 40), (420, 110)],
            "Y": [(440, 40), (500, 110)],
            "U": [(520, 40), (580, 110)],
            "I": [(600, 40), (660, 110)],
            "O": [(680, 40), (740, 110)],
            "P": [(760, 40), (820, 110)],
            "A": [(30, 120), (100, 190)],
            "S": [(120, 120), (180, 190)],
            "D": [(200, 120), (260, 190)],
            "F": [(280, 120), (340, 190)],
            "G": [(360, 120), (420, 190)],
            "H": [(440, 120), (500, 190)],
            "J": [(520, 120), (580, 190)],
            "K": [(600, 120), (660, 190)],
            "L": [(680, 120), (740, 190)],
            "Z": [(30, 200), (100, 270)],
            "X": [(120, 200), (180, 270)],
            "C": [(200, 200), (260, 270)],
            "V": [(280, 200), (340, 270)],
            "B": [(360, 200), (420, 270)],
            "N": [(440, 200), (500, 270)],
            "M": [(520, 200), (580, 270)],

            "Spc": [(600, 210), (700, 280)],  # Boşluk tuşu
            "Bck": [(720, 210), (820, 280)],  # Hepsini Silme

            "Del": [(860, 200), (940, 270)],  # Geri silme (Backspace) tuşu
            "Mod": [(860, 120), (940, 190)],  # mouse ye geçmek için oluşturulan button

            "Gog": [(1010, 200), (1095, 260)],  # Google'a git butonu
            "Ara": [(1010, 280), (1090, 340)],  # Ara (Enter) butonu
            "Ent": [(1010, 360), (1090, 420)]  # Enter butonu
        }
        self.basildi = {}
        self.yazi = ""

    def google_ac(self):
        webbrowser.open("https://www.google.com.tr")

    def arama(self):
        pyautogui.write(self.yazi)

    def space_tusu(self):
        self.yazi += " "
        pyautogui.press('space')

    def del_tusu(self):
        self.yazi = ""
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')

    def mod_degistir(self):
        self.yazi = ""  # Yazıyı temizle
        print( " kapatma işlemi 3 Saniye içerinde  gerçekleştiriliyor" )
        nesne=mouse()
        print(" visual mause sayafası çalışmaya başlıyor ")
        nesne.run()
        time.sleep(3)

        sys.exit()
        #        os.system("C:\\Users\\Sabri\\OneDrive\\Masaüstü\\orginal2opencv\\mouseclass.py")  # Moda atanmış uygulamayı aç
        #        pyautogui.press('q')

    def ara_enter(self):
        pyautogui.press('enter')

    def run(self):
        with self.el.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as eller:
            while True:
                _, fream = self.Webcam.read()
                fream = cv2.flip(fream, 1)
                rgb = cv2.cvtColor(fream, cv2.COLOR_BGR2RGB)

                result = eller.process(rgb)
                yukseklik, genislik, _ = fream.shape

                if result.multi_hand_landmarks:
                    for cizim in result.multi_hand_landmarks:
                        kordinat1 = cizim.landmark[8]
                        kordinat2 = cizim.landmark[12]
                        x1 = int(kordinat1.x * genislik)
                        y1 = int(kordinat1.y * yukseklik)

                        x2 = int(kordinat2.x * genislik)
                        y2 = int(kordinat2.y * yukseklik)

                        cv2.circle(fream, (x1, y1), 4, (255, 0, 0), 11)
                        cv2.circle(fream, (x2, y2), 4, (255, 255, 0), 11)

                        for harf, korfinatlar in self.klavye.items():
                            x_min, y_min = korfinatlar[0]
                            x_max, y_max = korfinatlar[1]

                            if x_min <= x1 <= x_max and y_min <= y1 <= y_max and x_min <= x2 <= x_max and y_min <= y2 <= y_max:
                                cv2.rectangle(fream, (x_min, y_min), (x_max, y_max), (0, 0, 255), -1)
                                if harf not in self.basildi or not self.basildi[harf]:
                                    print(harf)
                                    self.basildi[harf] = True
                                    if harf == "Del":
                                        self.del_tusu()
                                        continue
                                    elif harf == "Spc":
                                        self.space_tusu()
                                        continue
                                    elif harf == "Bck":
                                        if self.yazi:
                                            self.yazi = self.yazi[:-1]

                                    elif harf == "Ara":
                                        self.arama()
                                        continue
                                    elif harf == "Gog":
                                        self.google_ac()
                                        continue
                                    elif harf == "Ent":
                                        self.ara_enter()
                                        continue
                                    elif harf == "Mod":
                                        print("Mod Değiştiriliyor")
                                        self.mod_degistir()
                                    else:
                                        self.yazi += harf
                                    pyautogui.write(harf)
                                    self.basildi[harf] = True

                            else:
                                self.basildi[harf] = False

                for harf, korfinatlar in self.klavye.items():
                    x_min, y_min = korfinatlar[0]
                    x_max, y_max = korfinatlar[1]
                    cv2.rectangle(fream, (x_min, y_min), (x_max, y_max), (0, 0, 255), 3)
                    cv2.putText(fream, harf, (x_min + 20, y_min + 40), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

                cv2.rectangle(fream, (20, 280), (500, 320), (0, 0, 0), -1)
                cv2.putText(fream, self.yazi, (20, 310), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow('goruntu', fream)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

        self.Webcam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    EllerleKlavye().run()
