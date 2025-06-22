# services/profile_service.py

from database import user_repository

class ProfileService:
    """
    Este serviço lida com a lógica de negócio relacionada aos perfis dos usuários.
    """
    def update_user_profile(self, new_data):
        """
        Valida e solicita a atualização dos dados do perfil de um usuário no repositório.

        Args:
            new_data (dict): Um dicionário com os novos dados do usuário, incluindo o 'id'.

        Returns:
            tuple: Uma tupla contendo (True/False para sucesso, mensagem_string).
        """
        user_id = new_data.get('id')
        if not user_id:
            return False, "ID do usuário não fornecido para a atualização."
        
        # Futuramente, você pode adicionar mais validações aqui (ex: verificar se o email é válido).
        
        success = user_repository.update_profile(new_data)
        
        if success:
            return True, "Perfil atualizado com sucesso!"
        else:
            return False, "Falha ao atualizar o perfil no banco de dados."
