# database/comment_repository.py
from .connection import db_cursor
from datetime import datetime
import uuid

def create_comment(post_id, user_id, content):
    """
    Insere um novo comentário na tabela 'comments'.
    A estrutura da query é baseada na definição da tabela no arquivo SQL.
    """
    with db_cursor(commit=True) as cursor:
        if not cursor or not content or not content.strip():
            return None
        
        comment_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        sql = """
        INSERT INTO comments (id, post_id, user_id, content, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (comment_id, post_id, user_id, content, created_at))
        return comment_id

def fetch_by_post_id(post_id):
    """
    Busca todos os comentários de um post específico, ordenados por data.
    Junta com a tabela de usuários para obter os dados do autor.
    """
    with db_cursor() as cursor:
        if not cursor:
            return []
        
        sql = """
        SELECT 
            c.id, c.content, c.created_at,
            u.id AS author_id, u.username AS author_username,
            u.display_name AS author_display_name, u.profile_picture_url
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = %s
        ORDER BY c.created_at ASC
        """
        cursor.execute(sql, (post_id,))
        return cursor.fetchall()
