import os
from PIL import Image, ImageDraw, ImageFont
from config import Config

def generate_default_assets():
    """Cria os ícones e avatares padrão se eles não existirem."""
    if not os.path.exists(Config.DEFAULT_AVATAR_PATH):
        try:
            img = Image.new('RGB', (Config.PROFILE_PIC_SIZE, Config.PROFILE_PIC_SIZE), '#dddddd')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()
            draw.text((35, 45), "Avatar", fill="black", font=font)
            img.save(Config.DEFAULT_AVATAR_PATH)
            print(f"Asset gerado: {Config.DEFAULT_AVATAR_PATH}")
        except Exception as e:
            print(f"Aviso: Não foi possível criar o avatar padrão: {e}")

    if not os.path.exists(Config.VERIFIED_ICON_PATH):
        try:
            img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0, 19, 19), fill=Config.COLOR_ACCENT_LIGHT)
            draw.line([(4, 11), (8, 15), (16, 6)], fill='white', width=2)
            img.save(Config.VERIFIED_ICON_PATH)
            print(f"Asset gerado: {Config.VERIFIED_ICON_PATH}")
        except Exception as e:
            print(f"Aviso: Não foi possível criar o ícone de verificado: {e}")

    if not os.path.exists(Config.APP_ICON_PATH):
        try:
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0, 31, 31), fill=Config.COLOR_ACCENT_LIGHT)
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except IOError:
                font = ImageFont.load_default()
            draw.text((4, 0), "D", font=font, fill="white")
            img.save(Config.APP_ICON_PATH)
            print(f"Asset gerado: {Config.APP_ICON_PATH}")
        except Exception as e:
            print(f"Aviso: Não foi possível criar o ícone do aplicativo: {e}")
