"""
Módulo de gestión de base de datos SQLite
Maneja la creación y operaciones de la base de datos
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, List
from pathlib import Path

class DatabaseManager:
    """Gestor de base de datos SQLite para el sistema de reportes"""
    
    def __init__(self, db_path: str = "data/reportes.db"):
        self.db_path = db_path
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Asegura que el directorio de datos existe"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def initialize_database(self):
        """Inicializa la base de datos con todas las tablas necesarias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    company TEXT,
                    address TEXT,
                    city TEXT,
                    country TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de reportes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    report_type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            """)
            
            # Tabla de datos de reportes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS report_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id INTEGER NOT NULL,
                    field_name TEXT NOT NULL,
                    field_value TEXT,
                    field_type TEXT DEFAULT 'text',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (report_id) REFERENCES reports (id)
                )
            """)
            
            conn.commit()
    
    def create_client(self, name: str, email: str, phone: str = None, 
                     company: str = None, address: str = None, 
                     city: str = None, country: str = None) -> int:
        """Crea un nuevo cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clients (name, email, phone, company, address, city, country)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, company, address, city, country))
            conn.commit()
            return cursor.lastrowid
    
    def get_client(self, client_id: int) -> Optional[Dict]:
        """Obtiene un cliente por ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def get_all_clients(self) -> List[Dict]:
        """Obtiene todos los clientes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def update_client(self, client_id: int, **kwargs) -> bool:
        """Actualiza un cliente"""
        if not kwargs:
            return False
        
        # Agregar timestamp de actualización
        kwargs['updated_at'] = datetime.now().isoformat()
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [client_id]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE clients 
                SET {set_clause}
                WHERE id = ?
            """, values)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_client(self, client_id: int) -> bool:
        """Elimina un cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def create_report(self, client_id: int, title: str, description: str = None, 
                     report_type: str = "general") -> int:
        """Crea un nuevo reporte"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reports (client_id, title, description, report_type)
                VALUES (?, ?, ?, ?)
            """, (client_id, title, description, report_type))
            conn.commit()
            return cursor.lastrowid
    
    def get_reports_by_client(self, client_id: int) -> List[Dict]:
        """Obtiene todos los reportes de un cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, c.name as client_name 
                FROM reports r 
                JOIN clients c ON r.client_id = c.id 
                WHERE r.client_id = ?
                ORDER BY r.created_at DESC
            """, (client_id,))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def get_all_reports(self) -> List[Dict]:
        """Obtiene todos los reportes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, c.name as client_name 
                FROM reports r 
                JOIN clients c ON r.client_id = c.id 
                ORDER BY r.created_at DESC
            """)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def get_client_stats(self) -> Dict:
        """Obtiene estadísticas de clientes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total de clientes
            cursor.execute("SELECT COUNT(*) FROM clients")
            total_clients = cursor.fetchone()[0]
            
            # Clientes por país
            cursor.execute("""
                SELECT country, COUNT(*) as count 
                FROM clients 
                WHERE country IS NOT NULL 
                GROUP BY country 
                ORDER BY count DESC
            """)
            clients_by_country = dict(cursor.fetchall())
            
            # Clientes por ciudad
            cursor.execute("""
                SELECT city, COUNT(*) as count 
                FROM clients 
                WHERE city IS NOT NULL 
                GROUP BY city 
                ORDER BY count DESC
                LIMIT 10
            """)
            clients_by_city = dict(cursor.fetchall())
            
            return {
                'total_clients': total_clients,
                'clients_by_country': clients_by_country,
                'clients_by_city': clients_by_city
            }
    
    def get_report_stats(self) -> Dict:
        """Obtiene estadísticas de reportes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total de reportes
            cursor.execute("SELECT COUNT(*) FROM reports")
            total_reports = cursor.fetchone()[0]
            
            # Reportes por estado
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM reports 
                GROUP BY status
            """)
            reports_by_status = dict(cursor.fetchall())
            
            # Reportes por tipo
            cursor.execute("""
                SELECT report_type, COUNT(*) as count 
                FROM reports 
                GROUP BY report_type
            """)
            reports_by_type = dict(cursor.fetchall())
            
            return {
                'total_reports': total_reports,
                'reports_by_status': reports_by_status,
                'reports_by_type': reports_by_type
            }
