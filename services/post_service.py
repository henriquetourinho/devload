# services/post_service.py

from database import post_repository, reaction_repository

class PostService:
    """
    Este serviço lida com a lógica de negócio relacionada a posts,
    como criação, curtidas, etc.
    """
    def create_new_post(self, user_id, post_data):
        """
        Valida e solicita a criação de um novo post no repositório.

        Args:
            user_id (str): O ID do usuário que está criando o post.
            post_data (dict): Um dicionário com os dados do post (título, conteúdo, etc.).

        Returns:
            tuple: Uma tupla contendo (ID do novo post ou None, mensagem_string).
        """
        content = post_data.get('content')
        if not content:
            return None, "O conteúdo do post não pode ser vazio."
        
        # Chama a função do repositório para inserir no banco de dados
        post_id = post_repository.create_post(
            user_id=user_id,
            title=post_data.get('title'),
            content=content,
            post_type=post_data.get('post_type', 'text') # Define 'text' como padrão
            # No futuro, você pode expandir para passar 'media_url', 'code_snippet', etc.
        )
        
        if post_id:
            return post_id, "Post publicado com sucesso!"
        
        return None, "Ocorreu um erro ao publicar o post."

    def toggle_post_like(self, user_id, post_id):
        """Processa a ação de curtir/descurtir um post."""
        return reaction_repository.toggle_like(user_id, post_id)
        
    def get_post_like_count(self, post_id):
        """Obtém a contagem de curtidas de um post."""
        return reaction_repository.get_like_count(post_id)
        
    def is_post_liked_by_user(self, user_id, post_id):
        """Verifica se o usuário atual já curtiu o post."""
        return reaction_repository.is_liked_by_user(user_id, post_id)
