# config.py.example
# Copie este arquivo para config.py e preencha com suas informações locais.
# Lembre-se de adicionar config.py ao seu .gitignore!

import os

class Config:
    # Use variáveis de ambiente em produção, com fallbacks para desenvolvimento local.
    # Preencha os valores padrão com suas informações locais.
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "SUA_SENHA_AQUI") # <-- TROQUE AQUI PELA SUA SENHA LOCAL
    DB_NAME = os.getenv("DB_NAME", "devload")
    
    # --- O resto das configurações permanece o mesmo ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    MEDIA_DIR = os.path.join(BASE_DIR, "media")

    DEFAULT_AVATAR_PATH = os.path.join(ASSETS_DIR, "default_avatar.png")
    VERIFIED_ICON_PATH = os.path.join(ASSETS_DIR, "verified_icon.png")
    APP_ICON_PATH = os.path.join(ASSETS_DIR, "devload_icon.png")
    MEDIA_POSTS_FOLDER = os.path.join(MEDIA_DIR, "posts")

    AVATAR_SIZE = 40
    PROFILE_PIC_SIZE = 120
    MAX_POST_IMAGE_WIDTH = 600

    COLOR_BG_LIGHT = "#ffffff"
    COLOR_BG_MEDIUM_LIGHT = "#f0f0f0"
    COLOR_TEXT_DARK = "#333333"
    COLOR_ACCENT_LIGHT = "#1DA1F2"
    COLOR_ERROR_LIGHT = "#dc3545"
    COLOR_SUCCESS_LIGHT = "#28a745"
    COLOR_BORDER_LIGHT = "#cccccc"
    COLOR_INPUT_BG_LIGHT = "#e0e0e0"
    COLOR_INPUT_TEXT_DARK = "#333333"

def initialize_directories():
    os.makedirs(Config.MEDIA_POSTS_FOLDER, exist_ok=True)
    os.makedirs(Config.ASSETS_DIR, exist_ok=True)