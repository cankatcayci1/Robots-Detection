import unittest
import os
import cv2
import numpy as np
from main import find_white_objects

class TestFindWhiteObjects(unittest.TestCase):

    def setUp(self):
        self.input_folder = "Konsol3/input"
        self.output_folder = "Konsol3/output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)



    def test_input_folder_exists(self):
        # Giriş klasörünün varlığını kontrol et
        self.assertTrue(os.path.exists(self.input_folder), "Giriş klasörü bulunamadı.")

    def test_output_folder_exists(self):
        # Çıkış klasörünün varlığını kontrol et
        self.assertTrue(os.path.exists(self.output_folder), "Çıkış klasörü bulunamadı.")



    def test_input_files_extension(self):
        # Giriş klasöründeki dosyaların uzantılarını kontrol et
        input_files = os.listdir(self.input_folder)
        for file in input_files:
            with self.subTest(file=file):
                self.assertTrue(file.endswith('.jpg'), f"{file} dosyasının uzantısı .jpg değil.")

    def test_output_files_extension(self):
        # Çıkış klasöründeki dosyaların uzantılarını kontrol et
        output_files = os.listdir(self.output_folder)
        for file in output_files:
            with self.subTest(file=file):
                self.assertTrue(file.endswith('.jpg'), f"{file} dosyasının uzantısı .jpg değil.")




    def test_invalid_input_folder(self):
        # Hatalı bir giriş klasörüyle beyaz dengesi uygulanınca hata alınması durumunu kontrol et
        with self.assertRaises(FileNotFoundError):
            find_white_objects("invalid_input_folder", self.output_folder,200,255)



    def test_input_output_file_counts(self):
        # Beyaz dengesi uygulandıktan sonra giriş ve çıkış klasörlerindeki dosya sayılarını karşılaştırma
        find_white_objects(self.input_folder, self.output_folder,200,255)

        # Giriş ve çıkış klasörlerindeki dosya sayılarını al
        input_file_count = len(os.listdir(self.input_folder))
        output_file_count = len(os.listdir(self.output_folder))

        # Dosya sayılarını karşılaştır
        self.assertEqual(input_file_count, output_file_count, "Giriş ve çıkış klasörlerindeki dosya sayıları farklı.")




    def test_input_output_file_names(self):
        # Beyaz dengesi uygulandıktan sonra giriş ve çıkış klasörlerindeki dosya isimlerini karşılaştırma
        find_white_objects(self.input_folder, self.output_folder,200,255)

        # Giriş ve çıkış klasörlerindeki dosya isimlerini al
        input_files = sorted(os.listdir(self.input_folder))
        output_files = sorted(os.listdir(self.output_folder))

        # Dosya isimlerini karşılaştır
        for input_file, output_file in zip(input_files, output_files):
            with self.subTest(input_file=input_file, output_file=output_file):
                self.assertEqual(input_file, output_file, "Giriş ve çıkış klasörlerindeki dosya isimleri farklı.")



    def test_output_folder_not_empty(self):
        # Beyaz dengesi uygulandıktan sonra çıkış klasörünün boş olmadığını kontrol et
        find_white_objects(self.input_folder, self.output_folder,200,255)
        output_files = os.listdir(self.output_folder)
        self.assertNotEqual(len(output_files), 0, "Çıkış klasörü boş, beklenen bir durum değil.")






    def test_output_files_size(self):
        # Beyaz dengesi uygulandıktan sonra çıkış klasöründeki dosyaların boyutlarını kontrol et
        find_white_objects(self.input_folder, self.output_folder,200,255)
        output_files = os.listdir(self.output_folder)

        for output_file in output_files:
            with self.subTest(output_file=output_file):
                output_path = os.path.join(self.output_folder, output_file)
                output_img = cv2.imread(output_path)
                height, width, _ = output_img.shape
                self.assertGreaterEqual(height, 100, "Çıkış dosyasının yüksekliği 100 pikselden küçük.")
                self.assertGreaterEqual(width, 100, "Çıkış dosyasının genişliği 100 pikselden küçük.")





    def test_image_difference(self):
        # Beyaz dengesi uygulandıktan sonra giriş ve çıkış klasörlerindeki dosyalar arasındaki farkı kontrol et
        find_white_objects(self.input_folder, self.output_folder,200,255)
        input_files = os.listdir(self.input_folder)
        output_files = os.listdir(self.output_folder)

        for input_file, output_file in zip(input_files, output_files):
            with self.subTest(input_file=input_file, output_file=output_file):
                input_path = os.path.join(self.input_folder, input_file)
                output_path = os.path.join(self.output_folder, output_file)

                input_img = cv2.imread(input_path)
                output_img = cv2.imread(output_path)

                # İlk ve son görüntüler arasındaki farkı kontrol et
                difference = cv2.absdiff(input_img, output_img)
                difference_sum = np.sum(difference)
            
                self.assertNotEqual(difference_sum, 0, "İlk ve son görüntüler arasında fark bulunmamalı.")


    def test_output_images_contours(self):
        # Beyaz dengesi uygulandıktan sonra çıkış klasöründeki dosyaların beyaz nesnelerin sınırlarını kontrol et
        find_white_objects(self.input_folder, self.output_folder,200,255)
        output_files = os.listdir(self.output_folder)

        for output_file in output_files:
            with self.subTest(output_file=output_file):
                output_path = os.path.join(self.output_folder, output_file)
                output_img = cv2.imread(output_path)
                gray_output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)

                # Çıkış dosyalarının beyaz nesnelerin sınırlarını belirle
                _, thresh_output = cv2.threshold(gray_output_img, 1, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                self.assertGreater(len(contours), 0, "Çıkış dosyaları beyaz nesnelerin sınırlarını belirlemiyor.")






if __name__ == '__main__':
    unittest.main()