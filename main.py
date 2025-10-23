#!/usr/bin/env python3
"""
Sistema CLI para Reportes de Clientes
Aplicación principal para gestión y generación de reportes de clientes
"""

import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import print as rprint

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import DatabaseManager
from src.auth import AuthManager
from src.cli_menus import MainMenu
from src.utils import clear_screen, show_banner

def main():
    """Función principal de la aplicación"""
    console = Console()
    
    try:
        # Mostrar banner de bienvenida
        show_banner()
        
        # Inicializar base de datos
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Inicializar sistema de autenticación
        auth_manager = AuthManager(db_manager)
        
        # Verificar si es la primera ejecución
        if not auth_manager.user_exists():
            console.print("\n[bold blue]¡Bienvenido! Es la primera vez que ejecutas la aplicación.[/bold blue]")
            console.print("Necesitamos crear un usuario administrador.")
            
            username = Prompt.ask("Ingresa tu nombre de usuario")
            password = Prompt.ask("Ingresa tu contraseña", password=True)
            
            auth_manager.create_user(username, password, is_admin=True)
            console.print("[green]✓ Usuario administrador creado exitosamente[/green]")
        
        # Iniciar menú principal
        main_menu = MainMenu(db_manager, auth_manager)
        main_menu.run()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Aplicación interrumpida por el usuario[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error inesperado: {str(e)}[/red]")
        console.print("[yellow]Revisa los logs para más detalles[/yellow]")
    finally:
        console.print("\n[blue]¡Gracias por usar el Sistema de Reportes de Clientes![/blue]")

if __name__ == "__main__":
    main()
