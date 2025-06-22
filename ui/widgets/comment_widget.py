# ui/widgets/comment_widget.py

import tkinter as tk
from tkinter import ttk
from config import Config
from utils.image_loader import load_image

class CommentWidget(ttk.Frame):
    """Um widget para exibir um único comentário."""
    def __init__(self, master, comment_data):
        super().__init__(master, style='Comment.TFrame', padding=(5, 8))
        self.comment_data = comment_data
        self.image_references = {}

        # Estilo para este widget
        style = ttk.Style()
        style.configure('Comment.TFrame', background=Config.COLOR_BG_LIGHT)

        self._build_widget()

    def _build_widget(self):
        # Avatar do autor do comentário
        avatar_path = self.comment_data.get('profile_picture_url')
        avatar_img = load_image(avatar_path, 25, is_round=True) # Avatar menor
        self.image_references['avatar'] = avatar_img
        
        avatar_label = tk.Label(self, image=avatar_img, bg=Config.COLOR_BG_LIGHT)
        avatar_label.pack(side="left", padx=(0, 8), anchor="nw")

        # Frame para o conteúdo do comentário
        content_frame = ttk.Frame(self, style='Comment.TFrame')
        content_frame.pack(side="left", fill="x", expand=True)

        author_name = self.comment_data.get('author_display_name') or self.comment_data.get('author_username')
        author_label = tk.Label(content_frame, text=author_name, font=("Arial", 10, "bold"), bg=Config.COLOR_BG_LIGHT)
        author_label.pack(anchor="w")

        comment_content = tk.Label(content_frame, text=self.comment_data['content'], wraplength=450, justify="left", bg=Config.COLOR_BG_LIGHT, font=("Arial", 10))
        comment_content.pack(anchor="w")
