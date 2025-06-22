import tkinter as tk
from config import initialize_directories
from ui.main_window import DevLoadApp
from utils.asset_generator import generate_default_assets

if __name__ == "__main__":
    # Garante que pastas e assets padrão existam antes de iniciar
    initialize_directories()
    generate_default_assets()
    
    # Inicia a aplicação
    root = tk.Tk()
    app = DevLoadApp(root)
    root.mainloop()
