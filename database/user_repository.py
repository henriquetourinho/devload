# database/user_repository.py

from .connection import db_cursor
from datetime import datetime
import uuid

def find_by_username(username):
    """
    Busca um usuário no banco de dados pelo seu nome de usuário.

    Args:
        username (str): O nome de usuário a ser buscado.

    Returns:
        dict: Um dicionário com os dados do usuário, ou None se não for encontrado.
    """
    with db_cursor() as cursor:
        if not cursor: return None
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        return cursor.fetchone()

def find_by_id(user_id):
    """
    Busca um usuário no banco de dados pelo seu ID único.

    Args:
        user_id (str): O ID do usuário a ser buscado.

    Returns:
        dict: Um dicionário com os dados do usuário, ou None se não for encontrado.
    """
    with db_cursor() as cursor:
        if not cursor: return None
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

def create_user(username, hashed_password, display_name, email, default_avatar):
    """
    Insere um novo usuário no banco de dados.

    Returns:
        True se o usuário for criado com sucesso.
        "duplicate" se o nome de usuário ou e-mail já existir.
        False em caso de outros erros.
    """
    with db_cursor(commit=True) as cursor:
        if not cursor: return False
        
        # Primeiro, verifica se o nome de usuário ou e-mail já existem
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            return "duplicate"

        user_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        sql = """
        INSERT INTO users (id, username, password_hash, display_name, email, profile_picture_url, created_at, account_status, is_verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'active', FALSE)
        """
        cursor.execute(sql, (user_id, username, hashed_password, display_name, email, default_avatar, created_at))
        return True

def update_profile(new_data):
    """
    Atualiza as informações de perfil de um usuário existente no banco de dados.

    Args:
        new_data (dict): Um dicionário contendo os novos dados do perfil.
                         Deve incluir a chave 'id' para identificar o usuário.
    Returns:
        True se a atualização for bem-sucedida, False caso contrário.
    """
    with db_cursor(commit=True) as cursor:
        if not cursor: return False
        
        # Usamos placeholders nomeados (ex: %(display_name)s) que correspondem
        # às chaves do dicionário 'new_data'.
        sql = """
        UPDATE users SET
            display_name = %(display_name)s,
            bio = %(bio)s,
            location = %(location)s,
            email = %(email)s,
            profile_picture_url = %(profile_picture_url)s,
            github_url = %(github_url)s,
            linkedin_url = %(linkedin_url)s,
            personal_website_url = %(personal_website_url)s,
            updated_at = NOW()
        WHERE id = %(id)s
        """
        
        try:
            cursor.execute(sql, new_data)
            return True
        except Exception as e:
            print(f"Erro ao atualizar o perfil: {e}")
            return False
