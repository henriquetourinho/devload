# ui/views/timeline_view.py

import tkinter as tk
from tkinter import ttk, scrolledtext
from config import Config
from ..widgets.post_widget import PostWidget

class TimelineView(ttk.Frame):
    def __init__(self, master, posts, current_user, callbacks):
        super().__init__(master, style='TFrame')
        self.posts = posts
        self.current_user = current_user
        self.callbacks = callbacks

        # Referências para os widgets do composer
        self.composer_widgets = {}

        self._build_widgets()

    # --- Métodos de Controle do Composer (NOVO) ---

    def _expand_composer(self, event=None):
        """Esconde o frame compacto e mostra o expandido."""
        self.compact_frame.pack_forget()
        self.expanded_frame.pack(fill="x", pady=(0, 15), padx=10)
        # Foca no campo de texto principal
        self.composer_widgets['content_text'].focus_set()

    def _collapse_composer(self):
        """Esconde o frame expandido e mostra o compacto."""
        self.expanded_frame.pack_forget()
        self.compact_frame.pack(fill="x", pady=(0, 15), padx=10)
        # Limpa os campos para a próxima vez
        self.composer_widgets['content_text'].delete(1.0, tk.END)
        self.composer_widgets['title_entry'].delete(0, tk.END)

    def _handle_publish(self):
        """Coleta os dados do composer e chama o callback para criar o post."""
        post_data = {
            'title': self.composer_widgets['title_entry'].get().strip(),
            'content': self.composer_widgets['content_text'].get(1.0, tk.END).strip(),
            'post_type': 'text' # Por enquanto, apenas texto
            # Adicionar lógica para outros tipos de post (imagem, código) aqui no futuro
        }
        
        # Chama a função principal que lida com a criação do post
        self.callbacks['create_post'](post_data)
        
        # Retrai o composer após a publicação
        self._collapse_composer()

    # --- Métodos de Rolagem do Mouse (Existente) ---
    def _on_mouse_wheel(self, event):
        if self.canvas: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    def _on_mouse_wheel_linux(self, event):
        if self.canvas:
            if event.num == 4: self.canvas.yview_scroll(-1, "units")
            elif event.num == 5: self.canvas.yview_scroll(1, "units")

    # --- Construção da Interface ---
    def _build_widgets(self):
        # --- 1. Barra Superior ---
        top_bar = ttk.Frame(self, style='TFrame', padding=(10, 5))
        top_bar.pack(fill="x", side="top", pady=(0, 10))
        display_name = self.current_user.get('display_name') or self.current_user['username']
        tk.Label(top_bar, text=f"Olá, {display_name}!", font=("Arial", 14, "bold"), bg=Config.COLOR_BG_LIGHT).pack(side="left")
        ttk.Button(top_bar, text="Sair", command=self.callbacks.get('logout')).pack(side="right", padx=5)
        ttk.Button(top_bar, text="Meu Perfil", command=lambda: self.callbacks['show_profile'](self.current_user['id'])).pack(side="right")

        # --- 2. Composer de Publicação (NOVO) ---
        # Frame Compacto (visível por padrão)
        self.compact_frame = ttk.Frame(self, style='TFrame')
        self.compact_frame.pack(fill="x", pady=(0, 15), padx=10)
        
        compact_entry = ttk.Entry(self.compact_frame, font=("Arial", 11))
        compact_entry.insert(0, "O que está acontecendo?")
        compact_entry.pack(fill="x", ipady=8)
        # O evento <FocusIn> é acionado quando o widget é clicado
        compact_entry.bind("<FocusIn>", self._expand_composer)

        # Frame Expandido (oculto por padrão)
        self.expanded_frame = ttk.Frame(self, style='Post.TFrame', padding=10, relief="solid", borderwidth=1)
        
        ttk.Label(self.expanded_frame, text="Título (Opcional):").pack(anchor="w")
        title_entry = ttk.Entry(self.expanded_frame, font=("Arial", 11))
        title_entry.pack(fill="x", pady=(0, 10))
        self.composer_widgets['title_entry'] = title_entry

        content_text = scrolledtext.ScrolledText(self.expanded_frame, height=5, font=("Arial", 11), wrap=tk.WORD)
        content_text.pack(fill="both", expand=True, pady=(0, 10))
        self.composer_widgets['content_text'] = content_text
        
        composer_actions = ttk.Frame(self.expanded_frame, style='Post.TFrame')
        composer_actions.pack(fill="x")
        
        ttk.Button(composer_actions, text="Publicar", command=self._handle_publish).pack(side="right")
        ttk.Button(composer_actions, text="Cancelar", command=self._collapse_composer).pack(side="right", padx=10)

        # --- 3. Área de Rolagem para os Posts (Existente) ---
        self.canvas = tk.Canvas(self, bg=Config.COLOR_BG_LIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollable_frame = ttk.Frame(self.canvas, style='TFrame')
        scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel_linux)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10,0))
        scrollbar.pack(side="right", fill="y")
        
        if not self.posts:
            tk.Label(scrollable_frame, text="Nenhuma publicação para exibir.", bg=Config.COLOR_BG_LIGHT, font=("Arial", 12)).pack(pady=30)
        else:
            for post in self.posts:
                post_widget = PostWidget(scrollable_frame, post, self.callbacks)
                post_widget.pack(fill="x", pady=5, padx=10)
