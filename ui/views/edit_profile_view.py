# ui/views/edit_profile_view.py

import tkinter as tk
from tkinter import ttk, scrolledtext
from config import Config

class EditProfileView(tk.Toplevel):
    """
    Uma janela Toplevel (popup) que funciona como um formulário para editar o perfil do usuário.
    """
    def __init__(self, master, profile_data, save_callback):
        super().__init__(master)
        self.profile_data = profile_data
        self.save_callback = save_callback
        
        self.entries = {} # Dicionário para guardar os widgets de entrada
        
        self._configure_window()
        self._build_widgets()

    def _configure_window(self):
        self.title(f"Editando Perfil de @{self.profile_data['username']}")
        self.geometry("600x650")
        self.transient(self.master) # Mantém a janela sobre a principal
        self.grab_set() # Bloqueia a janela principal enquanto esta estiver aberta

    def _build_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Função auxiliar para criar linhas do formulário
        def create_form_row(label_text, key):
            ttk.Label(main_frame, text=label_text, font=("Arial", 11)).pack(anchor="w")
            entry = ttk.Entry(main_frame, font=("Arial", 11), width=60)
            entry.insert(0, self.profile_data.get(key) or "")
            entry.pack(anchor="w", fill="x", pady=(0, 10))
            self.entries[key] = entry # Salva a referência do widget

        # Criando os campos do formulário
        create_form_row("Nome de Exibição:", 'display_name')
        create_form_row("Localização:", 'location')
        create_form_row("Email:", 'email')
        create_form_row("URL da Foto de Perfil:", 'profile_picture_url')
        create_form_row("URL do GitHub:", 'github_url')
        create_form_row("URL do LinkedIn:", 'linkedin_url')
        create_form_row("URL do Website Pessoal:", 'personal_website_url')

        # Campo de Bio (com caixa de texto rolável)
        ttk.Label(main_frame, text="Bio:", font=("Arial", 11)).pack(anchor="w")
        bio_text = scrolledtext.ScrolledText(main_frame, height=5, font=("Arial", 11), wrap=tk.WORD)
        bio_text.insert(tk.END, self.profile_data.get('bio') or "")
        bio_text.pack(anchor="w", fill="both", expand=True, pady=(0, 15))
        self.entries['bio'] = bio_text

        # Botão Salvar
        save_button = ttk.Button(main_frame, text="Salvar Alterações", command=self._on_save)
        save_button.pack(pady=10)

    def _on_save(self):
        """Coleta os dados dos campos e chama o callback para salvar."""
        new_data = {}
        for key, widget in self.entries.items():
            if isinstance(widget, scrolledtext.ScrolledText):
                new_data[key] = widget.get(1.0, tk.END).strip()
            else:
                new_data[key] = widget.get().strip()
        
        # Adiciona o ID do usuário aos dados para saber quem atualizar
        new_data['id'] = self.profile_data['id']
        
        self.save_callback(new_data)
        self.destroy() # Fecha a janela de edição
