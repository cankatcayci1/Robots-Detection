import cv2
import numpy as np
import os
import argparse

def detect_and_draw_circles(input_folder, output_folder,param1,param2,minRad,maxRad):
    # Klasördeki tüm dosyaları listele
    image_files = os.listdir(input_folder)
    
    for file_name in image_files:
        # Dosya yolunu oluştur
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Resmi oku
        img = cv2.imread(input_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.blur(gray, (3, 3))

        detected_circles = cv2.HoughCircles(gray_blurred,  
                           cv2.HOUGH_GRADIENT, 1, 100, param1=param1, 
                           param2=param2, minRadius=minRad, maxRadius=maxRad)

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

            # Çıktıyı kaydet
            cv2.imwrite(output_path, img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Beyaz renge göre renk eşitleme')
    parser.add_argument('-i', '--input_folder', type=str, help='Konsol5\input', required=True)
    parser.add_argument('-o', '--output_folder', type=str, help='Konsol5\output', required=True)
    parser.add_argument('param1', type=int, default=75, nargs='?')
    parser.add_argument('param2', type=int, default=40, nargs='?')
    parser.add_argument('minRadius', type=int, default=95, nargs='?')
    parser.add_argument('maxRadius', type=int, default=195, nargs='?')
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder
    param1 = args.param1
    param2 = args.param2
    minRad = args.minRadius
    maxRad = args.maxRadius

    detect_and_draw_circles(input_folder, output_folder,param1,param2,minRad,maxRad)

