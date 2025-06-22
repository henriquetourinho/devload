# ui/widgets/post_widget.py

import tkinter as tk
from tkinter import ttk, scrolledtext
from config import Config
from utils.image_loader import load_image
from .comment_widget import CommentWidget # <-- Importa nosso novo widget

class PostWidget(ttk.Frame):
    def __init__(self, master, post_data, callbacks):
        super().__init__(master, style='Post.TFrame', padding=10, relief="solid", borderwidth=1)
        self.post_data = post_data
        self.callbacks = callbacks
        self.image_references = {}

        self.comment_section_visible = False
        self.comments_loaded = False

        self._build_widget()

    def toggle_comment_section(self):
        """Mostra/esconde a seção de comentários e carrega os comentários na primeira vez."""
        if self.comment_section_visible:
            self.comment_section_frame.pack_forget()
            self.comment_section_visible = False
        else:
            self.comment_section_frame.pack(fill="x", padx=5, pady=(10, 0), anchor="w")
            self.comment_section_visible = True
            
            # Carrega os comentários apenas na primeira vez que a seção é aberta
            if not self.comments_loaded:
                # Mostra um indicador de carregamento
                self.loading_label.pack()
                # Pede para a main_window buscar os comentários
                self.callbacks['fetch_comments'](self.post_data['id'], self)
    
    def display_comments(self, comments):
        """Recebe a lista de comentários e os exibe."""
        self.loading_label.pack_forget() # Esconde "Carregando..."
        
        # Limpa comentários antigos antes de adicionar novos
        for widget in self.comments_display_frame.winfo_children():
            widget.destroy()

        if not comments:
            tk.Label(self.comments_display_frame, text="Nenhum comentário ainda. Seja o primeiro!", bg=Config.COLOR_BG_LIGHT).pack()
        else:
            for comment in comments:
                comment_widget = CommentWidget(self.comments_display_frame, comment)
                comment_widget.pack(fill="x", pady=(0, 5))
        
        self.comments_loaded = True

    def _post_comment(self):
        content = self.comment_text.get(1.0, tk.END).strip()
        self.callbacks['create_comment'](self.post_data['id'], content, self)
        # Limpa e recarrega para mostrar o novo comentário
        self.comments_loaded = False
        self.toggle_comment_section() # Fecha
        self.toggle_comment_section() # E reabre para recarregar

    def _build_widget(self):
        # --- Frame do Cabeçalho e Conteúdo (sem alterações) ---
        # (código omitido por brevidade, é o mesmo de antes)
        header_frame = ttk.Frame(self, style='Post.TFrame')
        header_frame.pack(fill="x", pady=(0, 10), anchor="nw")
        avatar_path = self.post_data.get('profile_picture_url')
        avatar_img = load_image(avatar_path, Config.AVATAR_SIZE, is_round=True)
        self.image_references['avatar'] = avatar_img
        avatar_label = tk.Label(header_frame, image=avatar_img, bg=Config.COLOR_BG_MEDIUM_LIGHT)
        avatar_label.pack(side="left", padx=(0, 10))
        author_details_frame = ttk.Frame(header_frame, style='Post.TFrame')
        author_details_frame.pack(side="left", anchor="nw")
        author_display_name = self.post_data.get('author_display_name') or self.post_data['author_username']
        author_label = tk.Label(author_details_frame, text=author_display_name, font=("Arial", 12, "bold"), bg=Config.COLOR_BG_MEDIUM_LIGHT, fg=Config.COLOR_ACCENT_LIGHT, cursor="hand2")
        author_label.pack(side="top", anchor="w")
        author_label.bind("<Button-1>", lambda e: self.callbacks['show_profile'](self.post_data['author_id']))
        if self.post_data.get('title'):
            title_label = tk.Label(self, text=self.post_data['title'], font=("Arial", 14, "bold"), bg=Config.COLOR_BG_MEDIUM_LIGHT, wraplength=500, justify="left")
            title_label.pack(anchor="w", pady=(0, 5), padx=5)
        content_label = tk.Label(self, text=self.post_data['content'], font=("Arial", 11), bg=Config.COLOR_BG_MEDIUM_LIGHT, wraplength=500, justify="left")
        content_label.pack(anchor="w", pady=(0, 10), padx=5)
        # --- Fim do Frame do Cabeçalho e Conteúdo ---

        # --- Frame de Ações ---
        action_frame = ttk.Frame(self, style='Post.TFrame')
        action_frame.pack(fill="x", padx=5)
        
        initial_like_count = self.post_data.get('like_count', 0)
        self.like_button = ttk.Button(action_frame, text=f"Curtir ({initial_like_count})", command=lambda: self.callbacks['like_post'](self.post_data['id'], self))
        self.like_button.pack(side="left", padx=(0, 5))

        self.comment_button = ttk.Button(action_frame, text="Comentar", command=self.toggle_comment_section)
        self.comment_button.pack(side="left", padx=5)

        # --- Seção de Comentários (Inicialmente Oculta) ---
        self.comment_section_frame = ttk.Frame(self, style='Post.TFrame')
        
        # Área para exibir os comentários existentes
        self.comments_display_frame = ttk.Frame(self.comment_section_frame, style='TFrame')
        self.comments_display_frame.pack(fill="x", pady=10)
        self.loading_label = tk.Label(self.comments_display_frame, text="Carregando comentários...", bg=Config.COLOR_BG_LIGHT)

        # Separador
        ttk.Separator(self.comment_section_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Caixa para escrever um novo comentário
        self.comment_text = scrolledtext.ScrolledText(self.comment_section_frame, height=3, font=("Arial", 10), wrap=tk.WORD)
        self.comment_text.pack(fill="x", expand=True, pady=5)
        
        comment_action_frame = ttk.Frame(self.comment_section_frame, style='TFrame')
        comment_action_frame.pack(fill="x")
        
        ttk.Button(comment_action_frame, text="Postar Comentário", command=self._post_comment).pack(side="right")
        ttk.Button(comment_action_frame, text="Fechar", command=self.toggle_comment_section).pack(side="right", padx=10)

    def update_like_display(self, new_count, is_liked_by_current_user):
        self.like_button.config(text=f"Curtir ({new_count})")
