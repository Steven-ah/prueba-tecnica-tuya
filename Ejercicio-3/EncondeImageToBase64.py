import base64
import urllib.request

class EncondeImageToBase64():

    def __init__(self, url: str):
        self.url = url

    def get_image(self):
        """ Obtiene la imagen desde la URL brindada"""
        url_fixed = self.url.replace("\\", "")
        try:
            with urllib.request.urlopen(url_fixed) as response:
                if response.status != 200:
                    return None
                content = response.read()
                return content
        except Exception as e:
            print(f"Error al obtener la imagen desde {self.url}: {e}")
            return None
        
    def encode_to_base64(self):
        """ Convierte la imagen obtenida a base64"""
        image = self.get_image()
        if image is None:
            return None
        try:
            encoded_image = base64.b64encode(image).decode('utf-8')
            return encoded_image
        except Exception as e:
            print(f"Error al convertir la imagen a base64 desde {self.url}: {e}")
            return None
