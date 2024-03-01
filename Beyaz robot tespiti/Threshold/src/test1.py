import unittest
import os
import cv2
from main import white_balance

class TestWhiteBalance(unittest.TestCase):
    def setUp(self):
        # Test için gerekli klasörleri ve dosyaları oluştur
        self.input_folder = "Konsol1/input"
        self.output_folder = "Konsol1/output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)



    def test_white_balance(self):
        # Beyaz dengesi fonksiyonunu test et
        white_balance(self.input_folder, self.output_folder,200,255)

        # Çıkış klasöründe beklenen sayıda dosya olduğunu kontrol et
        output_files = os.listdir(self.output_folder)
        self.assertEqual(len(output_files), 32)

        # Her bir çıkış dosyasını kontrol et
        for i in range(1, 33):
            with self.subTest(i=i):
                output_path = f"{self.output_folder}/{i}.jpg"
                self.assertTrue(os.path.exists(output_path), f"{output_path} dosyası bulunamadı.")




    def test_input_folder_exists(self):
        # Giriş klasörünün varlığını kontrol et
        self.assertTrue(os.path.exists(self.input_folder), "Giriş klasörü bulunamadı.")

    def test_output_folder_exists(self):
        # Çıkış klasörünün varlığını kontrol et
        self.assertTrue(os.path.exists(self.output_folder), "Çıkış klasörü bulunamadı.")

    # Yeni testler ekleniyor
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

    def test_output_files_content(self):
        # Çıkış klasöründeki dosyaların içeriğini kontrol et
        output_files = os.listdir(self.output_folder)
        for file in output_files:
            with self.subTest(file=file):
                output_path = os.path.join(self.output_folder, file)
                img = cv2.imread(output_path)
                self.assertIsNotNone(img, f"{file} dosyası geçerli bir görüntü içermiyor.")

    def test_white_balance_output(self):
        # Beyaz dengesi uygulandıktan sonra çıkış dosyalarının içeriğini kontrol et
        white_balance(self.input_folder, self.output_folder,200,255)
        output_files = os.listdir(self.output_folder)
        for file in output_files:
            with self.subTest(file=file):
                output_path = os.path.join(self.output_folder, file)
                img = cv2.imread(output_path)
                self.assertIsNotNone(img, f"{file} dosyası geçerli bir görüntü içermiyor.")


    def test_invalid_input_folder(self):
        # Hatalı bir giriş klasörüyle beyaz dengesi uygulanınca hata alınması durumunu kontrol et
        with self.assertRaises(FileNotFoundError):
            white_balance("invalid_input_folder", self.output_folder,200,255)


    def test_input_output_file_counts(self):
        # Beyaz dengesi uygulandıktan sonra giriş ve çıkış klasörlerindeki dosya sayılarını karşılaştırma
        white_balance(self.input_folder, self.output_folder,200,255)

        # Giriş ve çıkış klasörlerindeki dosya sayılarını al
        input_file_count = len(os.listdir(self.input_folder))
        output_file_count = len(os.listdir(self.output_folder))

        # Dosya sayılarını karşılaştır
        self.assertEqual(input_file_count, output_file_count, "Giriş ve çıkış klasörlerindeki dosya sayıları farklı.")


    def test_input_output_file_names(self):
        # Beyaz dengesi uygulandıktan sonra giriş ve çıkış klasörlerindeki dosya isimlerini karşılaştırma
        white_balance(self.input_folder, self.output_folder,200,255)

        # Giriş ve çıkış klasörlerindeki dosya isimlerini al
        input_files = sorted(os.listdir(self.input_folder))
        output_files = sorted(os.listdir(self.output_folder))

        # Dosya isimlerini karşılaştır
        for input_file, output_file in zip(input_files, output_files):
            with self.subTest(input_file=input_file, output_file=output_file):
                self.assertEqual(input_file, output_file, "Giriş ve çıkış klasörlerindeki dosya isimleri farklı.")


if __name__ == "__main__":
    unittest.main()