# ui/views/profile_view.py

import tkinter as tk
from tkinter import ttk
import webbrowser  # Para abrir links
from config import Config
from utils.image_loader import load_image

class ProfileView(ttk.Frame):
    def __init__(self, master, profile_data, is_own_profile, back_callback, callbacks):
        super().__init__(master, style='TFrame', padding=20)
        self.profile_data = profile_data
        self.is_own_profile = is_own_profile
        self.back_callback = back_callback
        self.callbacks = callbacks # Dicionário de funções da janela principal
        self.image_references = {} # Para guardar referências de imagens

        self._build_widgets()

    def _open_link(self, url):
        """Abre uma URL no navegador padrão."""
        try:
            webbrowser.open_new(url)
        except Exception as e:
            print(f"Não foi possível abrir a URL {url}: {e}")

    def _build_widgets(self):
        # --- Botão Voltar ---
        back_button = ttk.Button(self, text="< Voltar para a Timeline", command=self.back_callback)
        back_button.pack(anchor="nw", pady=(0, 20))

        # --- Cabeçalho (Foto, Nome, Editar) ---
        header_frame = ttk.Frame(self, style='TFrame', relief="solid", borderwidth=1, padding=15)
        header_frame.pack(fill="x")

        # AÇÃO: Carregar a foto de perfil real
        avatar_path = self.profile_data.get('profile_picture_url')
        avatar_img = load_image(avatar_path, Config.PROFILE_PIC_SIZE, is_round=True)
        self.image_references['avatar'] = avatar_img
        
        avatar_label = tk.Label(header_frame, image=avatar_img, bg=Config.COLOR_BG_MEDIUM_LIGHT)
        avatar_label.pack(side="left", padx=(0, 20))

        info_frame = ttk.Frame(header_frame, style='TFrame')
        info_frame.pack(side="left", fill="x", expand=True)
        
        display_name = self.profile_data.get('display_name') or self.profile_data['username']
        tk.Label(info_frame, text=display_name, font=("Arial", 24, "bold"), bg=Config.COLOR_BG_LIGHT).pack(anchor="w")
        tk.Label(info_frame, text=f"@{self.profile_data['username']}", font=("Arial", 14), bg=Config.COLOR_BG_LIGHT).pack(anchor="w")

        # AÇÃO: Conectar o comando do botão de editar
        if self.is_own_profile:
            edit_button = ttk.Button(info_frame, text="Editar Perfil", command=lambda: self.callbacks['edit_profile'](self.profile_data))
            edit_button.pack(anchor="w", pady=10)

        # --- Detalhes (Bio, Localização, Links) ---
        details_frame = ttk.Frame(self, padding=(5, 20))
        details_frame.pack(fill="both", expand=True)

        # Função auxiliar para criar os campos de detalhes
        def create_detail_row(label_text, value, is_link=False):
            if value:
                row_frame = ttk.Frame(details_frame, style='TFrame')
                row_frame.pack(fill="x", pady=2)
                
                label = tk.Label(row_frame, text=label_text, font=("Arial", 11, "bold"), bg=Config.COLOR_BG_LIGHT)
                label.pack(side="left", anchor="nw", padx=(0, 5))
                
                if is_link:
                    value_label = tk.Label(row_frame, text=value, bg=Config.COLOR_BG_LIGHT, fg=Config.COLOR_ACCENT_LIGHT, cursor="hand2", justify="left", wraplength=700)
                    value_label.bind("<Button-1>", lambda e, url=value: self._open_link(url))
                else:
                    value_label = tk.Label(row_frame, text=value, bg=Config.COLOR_BG_LIGHT, justify="left", wraplength=700)
                
                value_label.pack(side="left", anchor="nw")

        # AÇÃO: Adicionar todos os campos do banco de dados
        create_detail_row("Bio:", self.profile_data.get('bio'))
        create_detail_row("Localização:", self.profile_data.get('location'))
        create_detail_row("Email:", self.profile_data.get('email'))
        create_detail_row("GitHub:", self.profile_data.get('github_url'), is_link=True)
        create_detail_row("LinkedIn:", self.profile_data.get('linkedin_url'), is_link=True)
        create_detail_row("Website:", self.profile_data.get('personal_website_url'), is_link=True)
