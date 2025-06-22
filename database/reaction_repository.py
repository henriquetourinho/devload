# database/reaction_repository.py
from .connection import db_cursor
import uuid

def toggle_like(user_id, post_id):
    with db_cursor(commit=True) as cursor:
        if not cursor: return False
        # Verifica se a curtida já existe
        cursor.execute("SELECT id FROM reactions WHERE user_id = %s AND post_id = %s AND reaction_type = 'like'", (user_id, post_id))
        exists = cursor.fetchone()
        
        if exists:
            # Se existe, remove
            cursor.execute("DELETE FROM reactions WHERE id = %s", (exists['id'],))
        else:
            # Se não existe, insere
            like_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO reactions (id, user_id, post_id, reaction_type) VALUES (%s, %s, %s, 'like')", (like_id, user_id, post_id))
        return True

def get_like_count(post_id):
    with db_cursor() as cursor:
        if not cursor: return 0
        cursor.execute("SELECT COUNT(*) as count FROM reactions WHERE post_id = %s AND reaction_type = 'like'", (post_id,))
        result = cursor.fetchone()
        return result['count'] if result else 0

def is_liked_by_user(user_id, post_id):
    with db_cursor() as cursor:
        if not cursor: return False
        cursor.execute("SELECT id FROM reactions WHERE user_id = %s AND post_id = %s AND reaction_type = 'like'", (user_id, post_id))
        return cursor.fetchone() is not None
