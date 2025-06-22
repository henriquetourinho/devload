# database/post_repository.py

from .connection import db_cursor
from datetime import datetime
import uuid

def fetch_timeline_posts():
    """Busca os posts para a timeline, ordenados por data de criação."""
    with db_cursor() as cursor:
        if not cursor: return []
        sql = """
            SELECT 
                p.id, p.content, p.post_type, p.media_url, p.code_snippet, p.code_language, 
                p.title, p.created_at, p.original_post_id,
                u.id AS author_id, u.username AS author_username, 
                u.display_name AS author_display_name, u.profile_picture_url, u.is_verified
            FROM posts p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
            LIMIT 50
        """
        cursor.execute(sql)
        posts = cursor.fetchall()
        return posts

def create_post(user_id, title, content, post_type, media_url=None, code_snippet=None, code_language=None):
    """Cria um novo post original no banco de dados."""
    with db_cursor(commit=True) as cursor:
        if not cursor: return None
        post_id = str(uuid.uuid4())
        timestamp = datetime.now()
        sql = """
        INSERT INTO posts (id, user_id, title, content, post_type, media_url, code_snippet, code_language, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (post_id, user_id, title, content, post_type, media_url, code_snippet, code_language, timestamp, timestamp))
        return post_id

def create_repost(user_id, original_post_id):
    """
    Cria um novo post que é um compartilhamento de um post existente.
    """
    with db_cursor(commit=True) as cursor:
        if not cursor: return None

        # 1. Busca os detalhes do post original
        cursor.execute("SELECT content, user_id FROM posts WHERE id = %s", (original_post_id,))
        original_post = cursor.fetchone()
        if not original_post:
            return None # Post original não encontrado

        # 2. Busca o nome do autor original
        cursor.execute("SELECT username FROM users WHERE id = %s", (original_post['user_id'],))
        original_author = cursor.fetchone()
        original_author_username = original_author['username'] if original_author else "usuário desconhecido"

        # 3. Cria o conteúdo para o novo post (o repost)
        new_content = f"Compartilhou uma publicação de @{original_author_username}:\n\n\"\"\"\n{original_post['content']}\n\"\"\""
        repost_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        # 4. Insere o novo post, marcando o 'original_post_id'
        # O post_type de um repost é 'text', pois seu conteúdo principal é o texto de compartilhamento.
        sql = """
        INSERT INTO posts (id, user_id, content, post_type, original_post_id, created_at)
        VALUES (%s, %s, %s, 'text', %s, %s)
        """
        cursor.execute(sql, (repost_id, user_id, new_content, original_post_id, created_at))
        return repost_id
