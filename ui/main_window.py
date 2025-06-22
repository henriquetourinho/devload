# ui/main_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from config import Config

# Importa os serviços e repositórios necessários para a lógica da aplicação
from services.auth_service import AuthService
from services.post_service import PostService
from services.profile_service import ProfileService
from services.comment_service import CommentService
from database import user_repository, post_repository, reaction_repository

class DevLoadApp:
    """
    A classe principal da aplicação. Gerencia a janela, o estado
    e a navegação entre as diferentes telas (Views).
    """
    def __init__(self, master):
        self.master = master
        
        # Instancia os serviços que a aplicação usará
        self.auth_service = AuthService()
        self.post_service = PostService()
        self.profile_service = ProfileService()
        self.comment_service = CommentService()
        
        # Variáveis de estado da aplicação
        self.current_user = None
        self.icon_photo = None # Para guardar a referência da imagem do ícone

        self._configure_window()
        self._configure_styles()

        # Frame principal que hospedará todas as outras telas
        self.main_frame = ttk.Frame(self.master, style='TFrame')
        self.main_frame.pack(fill="both", expand=True)

        # A aplicação começa na tela de login
        self.show_login_screen()

    # --- Métodos de Configuração Inicial ---

    def _configure_window(self):
        """Configura as propriedades da janela principal."""
        self.master.title("DevLoad - A Rede Social Dev")
        self.master.geometry("1000x700")
        self.master.minsize(800, 600)
        try:
            self.icon_photo = ImageTk.PhotoImage(Image.open(Config.APP_ICON_PATH))
            self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon_photo)
        except Exception as e:
            print(f"Aviso: não foi possível carregar o ícone do app: {e}")

    def _configure_styles(self):
        """Configura os estilos visuais da aplicação usando ttk."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('.', background=Config.COLOR_BG_LIGHT, foreground=Config.COLOR_TEXT_DARK)
        self.style.configure('TFrame', background=Config.COLOR_BG_LIGHT)
        self.style.configure('TLabel', background=Config.COLOR_BG_LIGHT, font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), background=Config.COLOR_ACCENT_LIGHT, foreground='white', padding=5)
        self.style.map('TButton', background=[('active', '#0056b3')])
        self.style.configure('TEntry', fieldbackground=Config.COLOR_INPUT_BG_LIGHT, foreground=Config.COLOR_INPUT_TEXT_DARK, insertbackground=Config.COLOR_INPUT_TEXT_DARK)

    # --- Métodos de Controle e Callbacks ---

    def _clear_frame(self):
        """Limpa o frame principal para trocar de tela."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def get_app_callbacks(self):
        """
        Cria o dicionário de callbacks para conectar a UI com a lógica.
        Este dicionário é passado para as Views filhas.
        """
        return {
            'show_profile': self.show_profile_screen,
            'like_post': self.handle_like_post,
            'edit_profile': self.handle_edit_profile,
            'logout': self.handle_logout,
            'create_post': self.handle_create_post,
            'create_comment': self.handle_create_comment,
            'fetch_comments': self.handle_fetch_comments
        }

    # --- Métodos de Navegação e Troca de Tela ---

    def show_login_screen(self):
        self._clear_frame()
        from .views.login_view import LoginView
        login_view = LoginView(self.main_frame, self.handle_login, self.show_register_screen)
        login_view.pack(fill="both", expand=True)

    def show_register_screen(self):
        self._clear_frame()
        tk.Label(self.main_frame, text="Tela de Registro (A ser implementada)", font=("Arial", 18)).pack(expand=True)
        ttk.Button(self.main_frame, text="Voltar para Login", command=self.show_login_screen).pack()

    def show_timeline_screen(self):
        self._clear_frame()
        from .views.timeline_view import TimelineView
        
        posts = post_repository.fetch_timeline_posts()
        for post in posts:
            post['like_count'] = reaction_repository.get_like_count(post['id'])
        
        callbacks = self.get_app_callbacks()
        timeline_view = TimelineView(self.main_frame, posts, self.current_user, callbacks)
        timeline_view.pack(fill="both", expand=True)

    def show_profile_screen(self, user_id):
        self._clear_frame()
        from .views.profile_view import ProfileView
        
        profile_data = user_repository.find_by_id(user_id)
        
        if profile_data:
            is_own_profile = (self.current_user['id'] == user_id)
            callbacks = self.get_app_callbacks()
            profile_view = ProfileView(self.main_frame, profile_data, is_own_profile, self.show_timeline_screen, callbacks)
            profile_view.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Erro de Perfil", f"Usuário com ID {user_id} não encontrado.")
            self.show_timeline_screen()

    # --- Métodos de Manipulação de Ações (Handlers) ---

    def handle_login(self, username, password):
        user, message = self.auth_service.login(username, password)
        if user:
            self.current_user = user
            self.show_timeline_screen()
        else:
            messagebox.showerror("Erro de Login", message)

    def handle_logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "Você foi desconectado com sucesso.")
        self.show_login_screen()

    def handle_like_post(self, post_id, post_widget_instance):
        if not self.current_user: return
        success = self.post_service.toggle_post_like(self.current_user['id'], post_id)
        if success:
            new_count = self.post_service.get_post_like_count(post_id)
            is_liked = self.post_service.is_post_liked_by_user(self.current_user['id'], post_id)
            post_widget_instance.update_like_display(new_count, is_liked)
        else:
            messagebox.showerror("Erro", "Não foi possível processar a curtida.")
    
    def handle_create_post(self, post_data):
        post_id, message = self.post_service.create_new_post(user_id=self.current_user['id'], post_data=post_data)
        if post_id:
            messagebox.showinfo("Sucesso", message)
            self.show_timeline_screen()
        else:
            messagebox.showerror("Erro", message)
    
    def handle_create_comment(self, post_id, content, post_widget_instance):
        success, message = self.comment_service.create_new_comment(post_id=post_id, user_id=self.current_user['id'], content=content)
        if success:
            messagebox.showinfo("Sucesso", message)
            post_widget_instance.toggle_comment_section(force_close=True)
        else:
            messagebox.showerror("Erro", message)

    def handle_edit_profile(self, profile_data):
        from .views.edit_profile_view import EditProfileView
        edit_window = EditProfileView(self.master, profile_data, self.handle_save_profile)
        
    def handle_save_profile(self, new_data):
        success, message = self.profile_service.update_user_profile(new_data)
        if success:
            messagebox.showinfo("Sucesso", message)
            if self.current_user['id'] == new_data['id']:
                self.current_user = user_repository.find_by_id(new_data['id'])
            self.show_profile_screen(new_data['id'])
        else:
            messagebox.showerror("Erro", message)

    def handle_fetch_comments(self, post_id, post_widget_instance):
        """Busca os comentários para um post e manda o widget exibi-los."""
        comments = self.comment_service.get_comments_for_post(post_id)
        # Chama um método no próprio widget para que ele se atualize com os dados
        post_widget_instance.display_comments(comments)
