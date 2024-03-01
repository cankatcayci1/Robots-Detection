import unittest
import os
import cv2
import numpy as np
from main import detect_and_draw_circles

class TestDetectandDrawCircles(unittest.TestCase):

    def setUp(self):
        self.input_folder = "Konsol5/input"
        self.output_folder = "Konsol5/output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)



    def test_input_folder_exists(self):
        # Giriş klasörünün varlığını kontrol et
        self.assertTrue(os.path.exists(self.input_folder), "Giriş klasörü bulunamadı.")

    def test_output_folder_exists(self):
        # Çıkış klasörünün varlığını kontrol et
        self.assertTrue(os.path.exists(self.output_folder), "Çıkış klasörü bulunamadı.")



    def test_output_folder_not_empty(self):
        # Beyaz dengesi uygulandıktan sonra çıkış klasörünün boş olmadığını kontrol et
        detect_and_draw_circles(self.input_folder, self.output_folder, 75, 40, 95, 195)
        output_files = os.listdir(self.output_folder)
        self.assertNotEqual(len(output_files), 0, "Çıkış klasörü boş, beklenen bir durum değil.")



    def test_input_files_non_empty(self):
        # Beyaz dengesi uygulandıktan sonra çıkış klasöründeki dosyaların boş olmamasını kontrol et
        detect_and_draw_circles(self.input_folder, self.output_folder, 75, 40, 95, 195)
        input_files = os.listdir(self.input_folder)
        self.assertTrue(len(input_files) > 0, "Girdi klasörü boş, beklenen bir durum değil.")





    def test_output_files_size(self):
        # Beyaz dengesi uygulandıktan sonra çıkış klasöründeki dosyaların boyutlarını kontrol et
        detect_and_draw_circles(self.input_folder, self.output_folder, 75, 40, 95, 195)
        output_files = os.listdir(self.output_folder)

        for output_file in output_files:
            with self.subTest(output_file=output_file):
                output_path = os.path.join(self.output_folder, output_file)
                file_size = os.path.getsize(output_path)  # Dosya boyutunu al

                # Dosya boyutunun 10 KB'dan büyük olduğunu kontrol et (istediğiniz değeri ayarlayabilirsiniz)
                self.assertGreater(file_size, 10 * 1024, "Çıkış dosyasının boyutu 10 KB'dan küçük.")



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





    def test_different_input_output_images(self):
        # Giriş ve çıkış görüntülerinin birbirinden farklı olması durumunda hata vermesini kontrol et
        detect_and_draw_circles(self.input_folder, self.output_folder, 75, 40, 95, 195)
        input_files = os.listdir(self.input_folder)
        output_files = os.listdir(self.output_folder)

        for input_file, output_file in zip(input_files, output_files):
            with self.subTest(input_file=input_file, output_file=output_file):
                input_path = os.path.join(self.input_folder, input_file)
                output_path = os.path.join(self.output_folder, output_file)

                input_img = cv2.imread(input_path)
                output_img = cv2.imread(output_path)

                # Giriş ve çıkış dosyalarının birbirinden farklı olup olmadığını kontrol et
                self.assertFalse(np.array_equal(input_img, output_img),
                            "Giriş ve çıkış dosyaları birbirinden farklı olmalı.")



    def test_all_input_files(self):
        # Tüm giriş dosyaları testi için detect_and_draw_circles fonksiyonunu çağır
        detect_and_draw_circles(self.input_folder, self.output_folder, 75, 40, 95, 195)

        # Çıkış dosyalarını kontrol et
        for i in range(1, 33):
            input_file_name = f"{i}.jpg"
            output_file_path = os.path.join(self.output_folder, input_file_name)
            self.assertTrue(os.path.exists(output_file_path), f"{input_file_name} için çıkış dosyası oluşturulamadı.")



    def test_invalid_input_folder(self):
        # Test with an invalid input folder
        with self.assertRaises(FileNotFoundError):
            detect_and_draw_circles("invalid_input_folder", self.output_folder, 75, 40, 95, 195)





if __name__ == '__main__':
    unittest.main()