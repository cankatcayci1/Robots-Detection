import cv2
import argparse
import os

def white_balance(input_folder, output_folder,th_min,th_max):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = os.listdir(input_folder)
    input_files = [file for file in input_files if file.endswith('.jpg')]

    for file in input_files:
        input_path = os.path.join(input_folder, file)
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, th_min, th_max, cv2.THRESH_BINARY)
        result = cv2.bitwise_and(img, img, mask=thresh)
        output_path = os.path.join(output_folder, file)
        cv2.imwrite(output_path, result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Beyaz renge göre renk eşitleme')
    parser.add_argument('-i', '--input_folder', type=str, help='Konsol1\input', required=True)
    parser.add_argument('-o', '--output_folder', type=str, help='Konsol1\output', required=True)
    parser.add_argument("thresholdMin", type=int, default = 200, nargs="?")
    parser.add_argument("thresholdMax", type=int, default = 255, nargs="?")
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder
    th_min = args.thresholdMin
    th_max = args.thresholdMax

    white_balance(input_folder, output_folder, th_min,th_max)