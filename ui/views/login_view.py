# /root/Laboratorio/devload/Python/noivo/ui/views/login_view.py

import tkinter as tk
from tkinter import ttk
from config import Config

class LoginView(ttk.Frame):
    def __init__(self, master, login_callback, register_callback):
        super().__init__(master, style='TFrame')
        self.login_callback = login_callback
        
        # Usamos um único frame container que será centralizado com .pack()
        # Isso é mais estável que usar .place() aqui.
        container = ttk.Frame(self, style='TFrame', padding=30)
        # expand=True garante que o container possa crescer e ocupar o espaço
        container.pack(expand=True) 

        # Todos os outros widgets vão dentro deste container centralizado
        tk.Label(container, text="Bem-vindo à DevLoad", font=("Arial", 22, "bold"), bg=Config.COLOR_BG_LIGHT, fg=Config.COLOR_TEXT_DARK).pack(pady=10)
        tk.Label(container, text="Faça Login", font=("Arial", 16), bg=Config.COLOR_BG_LIGHT, fg=Config.COLOR_TEXT_DARK).pack(pady=(0, 20))
        
        tk.Label(container, text="Usuário:", font=("Arial", 12), bg=Config.COLOR_BG_LIGHT, fg=Config.COLOR_TEXT_DARK).pack(pady=(5,0), anchor="w")
        self.username_entry = ttk.Entry(container, width=40, font=("Arial", 12))
        self.username_entry.pack(pady=(0,10), fill="x")

        tk.Label(container, text="Senha:", font=("Arial", 12), bg=Config.COLOR_BG_LIGHT, fg=Config.COLOR_TEXT_DARK).pack(pady=(5,0), anchor="w")
        self.password_entry = ttk.Entry(container, width=40, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=(0,10), fill="x")
        
        ttk.Button(container, text="Entrar", command=self._on_login_click, style='TButton').pack(pady=15, fill="x", ipady=5)
        ttk.Button(container, text="Ainda não tem conta? Cadastre-se", command=register_callback, style='TButton').pack(pady=5, fill="x", ipady=5)

    def _on_login_click(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        self.login_callback(username, password)
