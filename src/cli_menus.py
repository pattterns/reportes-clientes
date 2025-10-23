"""
Sistema de menús CLI interactivos
Maneja toda la interfaz de usuario de línea de comandos
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich import print as rprint
from typing import Optional
import sys

from .database import DatabaseManager
from .auth import AuthManager
from .utils import clear_screen, show_error, show_success, show_warning, show_info

class MainMenu:
    """Menú principal de la aplicación"""
    
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthManager):
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.console = Console()
        self.current_user = None
    
    def run(self):
        """Ejecuta el menú principal"""
        while True:
            clear_screen()
            self.show_main_menu()
            choice = Prompt.ask(
                "Selecciona una opción",
                choices=["1", "2", "3", "4", "5", "0"],
                default="1"
            )
            
            if choice == "1":
                self.login_menu()
            elif choice == "2":
                self.register_menu()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                self.show_help()
            elif choice == "5":
                self.show_system_info()
            elif choice == "0":
                self.exit_application()
    
    def show_main_menu(self):
        """Muestra el menú principal"""
        menu_text = """
        [bold blue]📊 SISTEMA CLI DE REPORTES DE CLIENTES[/bold blue]
        
        [bold]Opciones disponibles:[/bold]
        
        [cyan]1.[/cyan] 🔐 Iniciar Sesión
        [cyan]2.[/cyan] 📝 Registrar Usuario
        [cyan]3.[/cyan] ℹ️  Acerca de
        [cyan]4.[/cyan] ❓ Ayuda
        [cyan]5.[/cyan] 🔧 Información del Sistema
        [cyan]0.[/cyan] 🚪 Salir
        
        """
        
        if self.current_user:
            menu_text += f"\n[green]👤 Usuario actual: {self.current_user['username']}[/green]"
        
        self.console.print(Panel(
            menu_text,
            title="[bold blue]Menú Principal[/bold blue]",
            border_style="blue"
        ))
    
    def login_menu(self):
        """Menú de inicio de sesión"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]🔐 Iniciar Sesión[/bold blue]",
            border_style="blue"
        ))
        
        username = Prompt.ask("Nombre de usuario")
        password = Prompt.ask("Contraseña", password=True)
        
        user = self.auth_manager.authenticate_user(username, password)
        if user:
            self.current_user = user
            show_success(f"¡Bienvenido, {user['username']}!")
            self.dashboard_menu()
        else:
            show_error("Credenciales incorrectas")
            input("Presiona Enter para continuar...")
    
    def register_menu(self):
        """Menú de registro de usuario"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]📝 Registrar Nuevo Usuario[/bold blue]",
            border_style="blue"
        ))
        
        username = Prompt.ask("Nombre de usuario")
        password = Prompt.ask("Contraseña", password=True)
        confirm_password = Prompt.ask("Confirmar contraseña", password=True)
        
        if password != confirm_password:
            show_error("Las contraseñas no coinciden")
            input("Presiona Enter para continuar...")
            return
        
        is_admin = Confirm.ask("¿Es administrador?")
        
        if self.auth_manager.create_user(username, password, is_admin):
            show_success("Usuario creado exitosamente")
        else:
            show_error("Error al crear usuario (puede que ya exista)")
        
        input("Presiona Enter para continuar...")
    
    def dashboard_menu(self):
        """Dashboard principal después del login"""
        while True:
            clear_screen()
            self.show_dashboard()
            choice = Prompt.ask(
                "Selecciona una opción",
                choices=["1", "2", "3", "4", "5", "6", "0"],
                default="1"
            )
            
            if choice == "1":
                self.client_management_menu()
            elif choice == "2":
                self.report_management_menu()
            elif choice == "3":
                self.dashboard_stats_menu()
            elif choice == "4":
                self.export_menu()
            elif choice == "5":
                self.settings_menu()
            elif choice == "6":
                self.logout()
                break
            elif choice == "0":
                self.exit_application()
    
    def show_dashboard(self):
        """Muestra el dashboard principal"""
        # Obtener estadísticas rápidas
        client_stats = self.db_manager.get_client_stats()
        report_stats = self.db_manager.get_report_stats()
        
        dashboard_text = f"""
        [bold blue]📊 DASHBOARD PRINCIPAL[/bold blue]
        
        [bold]Estadísticas rápidas:[/bold]
        👥 Total de clientes: [green]{client_stats['total_clients']}[/green]
        📄 Total de reportes: [green]{report_stats['total_reports']}[/green]
        
        [bold]Opciones disponibles:[/bold]
        
        [cyan]1.[/cyan] 👥 Gestión de Clientes
        [cyan]2.[/cyan] 📄 Gestión de Reportes
        [cyan]3.[/cyan] 📊 Estadísticas y Dashboard
        [cyan]4.[/cyan] 📤 Exportar Datos
        [cyan]5.[/cyan] ⚙️  Configuración
        [cyan]6.[/cyan] 🚪 Cerrar Sesión
        [cyan]0.[/cyan] 🚪 Salir de la Aplicación
        
        """
        
        self.console.print(Panel(
            dashboard_text,
            title=f"[bold blue]Bienvenido, {self.current_user['username']}[/bold blue]",
            border_style="green"
        ))
    
    def client_management_menu(self):
        """Menú de gestión de clientes"""
        while True:
            clear_screen()
            self.console.print(Panel(
                "[bold blue]👥 Gestión de Clientes[/bold blue]",
                border_style="blue"
            ))
            
            choice = Prompt.ask(
                "Selecciona una opción",
                choices=["1", "2", "3", "4", "5", "0"],
                default="1"
            )
            
            if choice == "1":
                self.list_clients()
            elif choice == "2":
                self.add_client()
            elif choice == "3":
                self.edit_client()
            elif choice == "4":
                self.delete_client()
            elif choice == "5":
                self.search_clients()
            elif choice == "0":
                break
    
    def list_clients(self):
        """Lista todos los clientes"""
        clear_screen()
        clients = self.db_manager.get_all_clients()
        
        if not clients:
            show_warning("No hay clientes registrados")
            input("Presiona Enter para continuar...")
            return
        
        # Crear tabla
        table = Table(title="📋 Lista de Clientes")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Email", style="blue")
        table.add_column("Teléfono", style="yellow")
        table.add_column("Empresa", style="magenta")
        table.add_column("Ciudad", style="red")
        
        for client in clients:
            table.add_row(
                str(client['id']),
                client['name'],
                client['email'] or "N/A",
                client['phone'] or "N/A",
                client['company'] or "N/A",
                client['city'] or "N/A"
            )
        
        self.console.print(table)
        input("Presiona Enter para continuar...")
    
    def add_client(self):
        """Agrega un nuevo cliente"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]➕ Agregar Nuevo Cliente[/bold blue]",
            border_style="blue"
        ))
        
        name = Prompt.ask("Nombre completo")
        email = Prompt.ask("Email")
        phone = Prompt.ask("Teléfono (opcional)", default="")
        company = Prompt.ask("Empresa (opcional)", default="")
        address = Prompt.ask("Dirección (opcional)", default="")
        city = Prompt.ask("Ciudad (opcional)", default="")
        country = Prompt.ask("País (opcional)", default="")
        
        try:
            client_id = self.db_manager.create_client(
                name, email, phone or None, company or None,
                address or None, city or None, country or None
            )
            show_success(f"Cliente creado exitosamente con ID: {client_id}")
        except Exception as e:
            show_error(f"Error al crear cliente: {str(e)}")
        
        input("Presiona Enter para continuar...")
    
    def edit_client(self):
        """Edita un cliente existente"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]✏️ Editar Cliente[/bold blue]",
            border_style="blue"
        ))
        
        client_id = IntPrompt.ask("ID del cliente a editar")
        client = self.db_manager.get_client(client_id)
        
        if not client:
            show_error("Cliente no encontrado")
            input("Presiona Enter para continuar...")
            return
        
        self.console.print(f"[green]Editando cliente: {client['name']}[/green]")
        
        # Mostrar campos actuales y permitir edición
        new_name = Prompt.ask("Nombre", default=client['name'])
        new_email = Prompt.ask("Email", default=client['email'])
        new_phone = Prompt.ask("Teléfono", default=client['phone'] or "")
        new_company = Prompt.ask("Empresa", default=client['company'] or "")
        new_address = Prompt.ask("Dirección", default=client['address'] or "")
        new_city = Prompt.ask("Ciudad", default=client['city'] or "")
        new_country = Prompt.ask("País", default=client['country'] or "")
        
        try:
            success = self.db_manager.update_client(
                client_id,
                name=new_name,
                email=new_email,
                phone=new_phone or None,
                company=new_company or None,
                address=new_address or None,
                city=new_city or None,
                country=new_country or None
            )
            
            if success:
                show_success("Cliente actualizado exitosamente")
            else:
                show_error("Error al actualizar cliente")
        except Exception as e:
            show_error(f"Error al actualizar cliente: {str(e)}")
        
        input("Presiona Enter para continuar...")
    
    def delete_client(self):
        """Elimina un cliente"""
        clear_screen()
        self.console.print(Panel(
            "[bold red]🗑️ Eliminar Cliente[/bold red]",
            border_style="red"
        ))
        
        client_id = IntPrompt.ask("ID del cliente a eliminar")
        client = self.db_manager.get_client(client_id)
        
        if not client:
            show_error("Cliente no encontrado")
            input("Presiona Enter para continuar...")
            return
        
        self.console.print(f"[red]¿Estás seguro de eliminar al cliente: {client['name']}?[/red]")
        
        if Confirm.ask("Esta acción no se puede deshacer"):
            try:
                success = self.db_manager.delete_client(client_id)
                if success:
                    show_success("Cliente eliminado exitosamente")
                else:
                    show_error("Error al eliminar cliente")
            except Exception as e:
                show_error(f"Error al eliminar cliente: {str(e)}")
        
        input("Presiona Enter para continuar...")
    
    def search_clients(self):
        """Busca clientes"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]🔍 Buscar Clientes[/bold blue]",
            border_style="blue"
        ))
        
        search_term = Prompt.ask("Término de búsqueda")
        clients = self.db_manager.get_all_clients()
        
        # Filtrar clientes
        filtered_clients = [
            client for client in clients
            if search_term.lower() in client['name'].lower() or
               search_term.lower() in (client['email'] or '').lower() or
               search_term.lower() in (client['company'] or '').lower()
        ]
        
        if not filtered_clients:
            show_warning("No se encontraron clientes")
            input("Presiona Enter para continuar...")
            return
        
        # Mostrar resultados
        table = Table(title=f"🔍 Resultados para: {search_term}")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Email", style="blue")
        table.add_column("Empresa", style="magenta")
        
        for client in filtered_clients:
            table.add_row(
                str(client['id']),
                client['name'],
                client['email'] or "N/A",
                client['company'] or "N/A"
            )
        
        self.console.print(table)
        input("Presiona Enter para continuar...")
    
    def report_management_menu(self):
        """Menú de gestión de reportes"""
        self.console.print("📄 Gestión de Reportes - En desarrollo...")
        input("Presiona Enter para continuar...")
    
    def dashboard_stats_menu(self):
        """Menú de estadísticas del dashboard"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]📊 Estadísticas y Dashboard[/bold blue]",
            border_style="blue"
        ))
        
        # Obtener estadísticas
        client_stats = self.db_manager.get_client_stats()
        report_stats = self.db_manager.get_report_stats()
        
        # Mostrar estadísticas de clientes
        self.console.print("\n[bold green]👥 Estadísticas de Clientes:[/bold green]")
        self.console.print(f"Total de clientes: {client_stats['total_clients']}")
        
        if client_stats['clients_by_country']:
            self.console.print("\n[bold]Clientes por país:[/bold]")
            for country, count in list(client_stats['clients_by_country'].items())[:5]:
                self.console.print(f"  {country}: {count}")
        
        if client_stats['clients_by_city']:
            self.console.print("\n[bold]Top ciudades:[/bold]")
            for city, count in list(client_stats['clients_by_city'].items())[:5]:
                self.console.print(f"  {city}: {count}")
        
        # Mostrar estadísticas de reportes
        self.console.print(f"\n[bold green]📄 Estadísticas de Reportes:[/bold green]")
        self.console.print(f"Total de reportes: {report_stats['total_reports']}")
        
        if report_stats['reports_by_status']:
            self.console.print("\n[bold]Reportes por estado:[/bold]")
            for status, count in report_stats['reports_by_status'].items():
                self.console.print(f"  {status}: {count}")
        
        if report_stats['reports_by_type']:
            self.console.print("\n[bold]Reportes por tipo:[/bold]")
            for report_type, count in report_stats['reports_by_type'].items():
                self.console.print(f"  {report_type}: {count}")
        
        input("\nPresiona Enter para continuar...")
    
    def export_menu(self):
        """Menú de exportación de datos"""
        self.console.print("📤 Exportar Datos - En desarrollo...")
        input("Presiona Enter para continuar...")
    
    def settings_menu(self):
        """Menú de configuración"""
        self.console.print("⚙️ Configuración - En desarrollo...")
        input("Presiona Enter para continuar...")
    
    def logout(self):
        """Cierra la sesión del usuario"""
        self.current_user = None
        show_success("Sesión cerrada exitosamente")
        input("Presiona Enter para continuar...")
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        clear_screen()
        about_text = """
        [bold blue]📊 Sistema CLI de Reportes de Clientes[/bold blue]
        
        [bold]Versión:[/bold] 1.0.0
        [bold]Desarrollado por:[/bold] Marcos
        [bold]Descripción:[/bold] Sistema de gestión y generación de reportes de clientes
        
        [bold]Características:[/bold]
        • Gestión completa de clientes
        • Generación de reportes en múltiples formatos
        • Dashboard con estadísticas
        • Interfaz CLI intuitiva
        • Base de datos SQLite integrada
        
        [bold]Tecnologías:[/bold]
        • Python 3.8+
        • SQLite
        • Rich (interfaz CLI)
        • ReportLab (PDF)
        • Pandas (análisis de datos)
        """
        
        self.console.print(Panel(
            about_text,
            title="[bold blue]Acerca de[/bold blue]",
            border_style="blue"
        ))
        input("Presiona Enter para continuar...")
    
    def show_help(self):
        """Muestra la ayuda del sistema"""
        clear_screen()
        help_text = """
        [bold blue]❓ Ayuda del Sistema[/bold blue]
        
        [bold]Navegación:[/bold]
        • Usa los números para seleccionar opciones
        • Presiona Enter para confirmar
        • Usa Ctrl+C para salir en cualquier momento
        
        [bold]Gestión de Clientes:[/bold]
        • Agregar: Crea nuevos clientes con información completa
        • Editar: Modifica datos de clientes existentes
        • Eliminar: Borra clientes (acción irreversible)
        • Buscar: Encuentra clientes por nombre, email o empresa
        
        [bold]Reportes:[/bold]
        • Genera reportes en PDF, Excel y CSV
        • Personaliza el contenido y formato
        • Exporta datos para análisis externo
        
        [bold]Dashboard:[/bold]
        • Visualiza estadísticas en tiempo real
        • Analiza tendencias de clientes
        • Monitorea el estado de reportes
        """
        
        self.console.print(Panel(
            help_text,
            title="[bold blue]Ayuda[/bold blue]",
            border_style="blue"
        ))
        input("Presiona Enter para continuar...")
    
    def show_system_info(self):
        """Muestra información del sistema"""
        clear_screen()
        import platform
        import sys
        
        system_info = f"""
        [bold blue]🔧 Información del Sistema[/bold blue]
        
        [bold]Sistema Operativo:[/bold] {platform.system()} {platform.release()}
        [bold]Arquitectura:[/bold] {platform.machine()}
        [bold]Python:[/bold] {sys.version.split()[0]}
        [bold]Directorio de trabajo:[/bold] {sys.path[0]}
        [bold]Base de datos:[/bold] SQLite
        [bold]Interfaz:[/bold] CLI con Rich
        """
        
        self.console.print(Panel(
            system_info,
            title="[bold blue]Información del Sistema[/bold blue]",
            border_style="blue"
        ))
        input("Presiona Enter para continuar...")
    
    def exit_application(self):
        """Sale de la aplicación"""
        clear_screen()
        self.console.print(Panel(
            "[bold blue]¡Gracias por usar el Sistema de Reportes de Clientes![/bold blue]",
            border_style="blue"
        ))
        sys.exit(0)
