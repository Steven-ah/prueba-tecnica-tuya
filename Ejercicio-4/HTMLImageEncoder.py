import os
import re

from EncondeImageToBase64 import EncondeImageToBase64


class HTMLImageEncoder():

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.img_url_list = []
        self.converted_imgs = 0
        self.failed_imgs = 0

    def extract_imgs(self):
        """ Extrae las URLs de las imágenes desde los archivos HTML 
        en el directorio especificado."""
        # Nos aseguramos de tomar solo los archivos con extensión .html
        files = [f for f in os.listdir(self.file_path) if f.endswith('.html')]
        
        for file in files:
            with open(os.path.join(self.file_path, file), 'r', encoding='utf-8') as f:
                content = f.read()
                img_urls = re.findall(r'[\"\']([^\"\']+\.(?:jpg|jpeg|png|webp))[\"\']',
                                      content,
                                      flags=re.IGNORECASE)
                img_urls = list(set(img_urls))  # Eliminamos duplicados
                img_urls = self.filter_https_images(img_urls)
                self.img_url_list.append((file, img_urls))

    def replace_img_urls(self):
        """ Reemplaza las URLs de las imágenes en los archivos HTML con sus
        versiones codificadas en base64."""
        for file, urls in self.img_url_list:
            with open(os.path.join(self.file_path, file),
                      'r',
                      encoding='utf-8') as f:
                content = f.read()
            for url in urls:
                enconder = EncondeImageToBase64(url)
                encoded_image = enconder.encode_to_base64()
                if encoded_image:
                    content = content.replace(url, f"data:image/jpeg;base64,{encoded_image}")
                    self.converted_imgs += 1
                else:
                    self.failed_imgs += 1
            with open(os.path.join(f"{self.file_path}/encoded_files", file),
                      'w',
                      encoding='utf-8') as f:
                f.write(content)

    def encode_html_imgs(self):
        """ Crea el directorio para almacenar los archivos HTML con imágenes codificadas."""
        encoded_files_path = os.path.join(self.file_path, "encoded_files")
        if not os.path.exists(encoded_files_path):
            os.makedirs(encoded_files_path)
        self.extract_imgs()
        self.replace_img_urls()
        return {"success": self.converted_imgs, "fail": self.failed_imgs}


    def filter_https_images(self, url_list):
        """ Filtra las url obtenidas para conservar solo aquellas que provengan
        de distribuidores de contenido publico con HTTPs"""
        return list(filter(lambda x: re.match(r"^https:", x), url_list))