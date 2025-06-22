from database import user_repository
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

class AuthService:
    def login(self, username, password):
        """Valida credenciais. Retorna dados do usuário ou None."""
        if not username or not password:
            return None, "Usuário e senha são obrigatórios."

        user = user_repository.find_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return user, "Login bem-sucedido!"
        
        return None, "Usuário ou senha inválidos."

    def register(self, username, email, password, display_name):
        """Registra um novo usuário."""
        if not all([username, email, password]):
            return False, "Usuário, email e senha são obrigatórios."
        if len(password) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."
            
        hashed_password = generate_password_hash(password)
        result = user_repository.create_user(username, hashed_password, display_name, email, Config.DEFAULT_AVATAR_PATH)

        if result is True:
            return True, "Usuário cadastrado com sucesso!"
        elif result == "duplicate":
            return False, "Nome de usuário ou e-mail já existe."
        else:
            return False, "Ocorreu um erro inesperado no cadastro."
