import mysql.connector
from tkinter import messagebox
from contextlib import contextmanager
from config import Config

@contextmanager
def db_cursor(commit=False):
    """
    Gerenciador de contexto para conexão e cursor com o DB.
    O commit é feito explicitamente para ter mais controle.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor(dictionary=True)
        yield cursor
        if commit:
            conn.commit()
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
        # Idealmente, isso seria um log, não um messagebox, para desacoplar da UI.
        messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro: {err}")
        yield None # Retorna None em caso de erro
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
