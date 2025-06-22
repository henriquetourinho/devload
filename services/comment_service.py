# services/comment_service.py
from database import comment_repository

class CommentService:
    """
    Este serviço lida com a lógica de negócio relacionada a comentários.
    """
    def create_new_comment(self, post_id, user_id, content):
        """
        Valida e solicita a criação de um novo comentário.

        Args:
            post_id (str): ID do post que está sendo comentado.
            user_id (str): ID do usuário que está comentando.
            content (str): O texto do comentário.

        Returns:
            tuple: Uma tupla contendo (True/False para sucesso, mensagem_string).
        """
        if not content or not content.strip():
            return False, "O comentário não pode estar vazio."
        
        comment_id = comment_repository.create_comment(post_id, user_id, content)
        
        if comment_id:
            return True, "Comentário postado com sucesso!"
        else:
            return False, "Falha ao postar o comentário."

    def get_comments_for_post(self, post_id):
        """
        Busca os comentários para um determinado post.

        Args:
            post_id (str): O ID do post cujos comentários serão buscados.

        Returns:
            list: Uma lista de dicionários, cada um representando um comentário.
        """
        return comment_repository.fetch_by_post_id(post_id)
