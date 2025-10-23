"""
Módulo de autenticación
Maneja el login y registro de usuarios
"""

import bcrypt
import sqlite3
from typing import Optional, Dict
from .database import DatabaseManager

class AuthManager:
    """Gestor de autenticación de usuarios"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def hash_password(self, password: str) -> str:
        """Hashea una contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, username: str, password: str, is_admin: bool = False) -> bool:
        """Crea un nuevo usuario"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                hashed_password = self.hash_password(password)
                cursor.execute("""
                    INSERT INTO users (username, password_hash, is_admin)
                    VALUES (?, ?, ?)
                """, (username, hashed_password, is_admin))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Usuario ya existe
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Autentica un usuario"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, password_hash, is_admin 
                FROM users 
                WHERE username = ?
            """, (username,))
            row = cursor.fetchone()
            
            if row and self.verify_password(password, row[2]):
                return {
                    'id': row[0],
                    'username': row[1],
                    'is_admin': bool(row[3])
                }
            return None
    
    def user_exists(self) -> bool:
        """Verifica si existe al menos un usuario"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0] > 0
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Obtiene un usuario por nombre de usuario"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, is_admin, created_at 
                FROM users 
                WHERE username = ?
            """, (username,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'is_admin': bool(row[2]),
                    'created_at': row[3]
                }
            return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Cambia la contraseña de un usuario"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            
            if row and self.verify_password(old_password, row[0]):
                new_hash = self.hash_password(new_password)
                cursor.execute("""
                    UPDATE users SET password_hash = ? WHERE id = ?
                """, (new_hash, user_id))
                conn.commit()
                return True
            return False
