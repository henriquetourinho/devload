# utils/image_loader.py

import os
from PIL import Image, ImageTk, ImageDraw
from config import Config

def load_image(path, size, is_round=False):
    """
    Carrega uma imagem, a redimensiona e opcionalmente a torna redonda.
    Retorna um objeto PhotoImage compatível com o Tkinter.
    """
    try:
        if not path or not os.path.exists(path):
            # Se o caminho for inválido ou não existir, usa o avatar padrão
            path = Config.DEFAULT_AVATAR_PATH

        # .convert("RGBA") é importante para a máscara de arredondamento funcionar corretamente
        original_image = Image.open(path).convert("RGBA")

        # Redimensionamento mantendo a proporção
        original_image.thumbnail((size, size), Image.LANCZOS)
        
        if is_round:
            # Cria uma máscara circular
            mask = Image.new("L", original_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, original_image.size[0], original_image.size[1]), fill=255)
            
            # Aplica a máscara
            final_image = Image.new("RGBA", original_image.size)
            final_image.paste(original_image, (0, 0), mask)
            return ImageTk.PhotoImage(final_image)
        
        return ImageTk.PhotoImage(original_image)
        
    except Exception as e:
        print(f"Erro ao carregar imagem {path}: {e}")
        # Retorna um placeholder cinza em caso de erro extremo
        placeholder = Image.new('RGB', (size, size), 'grey')
        return ImageTk.PhotoImage(placeholder)