import cv2
import argparse
import os
import numpy as np

def find_white_objects(input_folder, output_folder,th_min,th_max):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = os.listdir(input_folder)
    input_files = [file for file in input_files if file.endswith('.jpg')]

    for file in input_files:
        input_path = os.path.join(input_folder, file)
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, th_min, th_max, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        output_path = os.path.join(output_folder, file)
        cv2.imwrite(output_path, img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Beyaz nesnelerin bölge tespiti')
    parser.add_argument('-i', '--input_folder', type=str, help='Konsol3\input', required=True)
    parser.add_argument('-o', '--output_folder', type=str, help='Konsol3\output', required=True)
    parser.add_argument("thresholdMin", type=int, default = 200, nargs="?")
    parser.add_argument("thresholdMax", type=int, default = 255, nargs="?")
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder
    th_min = args.thresholdMin
    th_max = args.thresholdMax

    find_white_objects(input_folder, output_folder,th_min,th_max)