"""
Utilidades generales del sistema
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

def clear_screen():
    """Limpia la pantalla del terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Muestra el banner de bienvenida"""
    console = Console()
    
    banner_text = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           📊 SISTEMA CLI DE REPORTES DE CLIENTES 📊          ║
    ║                                                              ║
    ║                    Gestión y Análisis                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel(
        banner_text,
        title="[bold blue]¡Bienvenido![/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))

def format_currency(amount: float, currency: str = "€") -> str:
    """Formatea un número como moneda"""
    return f"{amount:,.2f} {currency}"

def format_date(date_str: str) -> str:
    """Formatea una fecha para mostrar"""
    try:
        from datetime import datetime
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        return str(date_str)
    except:
        return str(date_str)

def validate_email(email: str) -> bool:
    """Valida un email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Valida un número de teléfono"""
    import re
    # Patrón para números de teléfono internacionales
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None

def get_file_size(file_path: str) -> str:
    """Obtiene el tamaño de un archivo formateado"""
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "N/A"

def ensure_directory(path: str):
    """Asegura que un directorio existe"""
    os.makedirs(path, exist_ok=True)

def get_project_root() -> str:
    """Obtiene la ruta raíz del proyecto"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def show_error(message: str):
    """Muestra un mensaje de error"""
    console = Console()
    console.print(f"[red]❌ Error: {message}[/red]")

def show_success(message: str):
    """Muestra un mensaje de éxito"""
    console = Console()
    console.print(f"[green]✅ {message}[/green]")

def show_warning(message: str):
    """Muestra un mensaje de advertencia"""
    console = Console()
    console.print(f"[yellow]⚠️  {message}[/yellow]")

def show_info(message: str):
    """Muestra un mensaje informativo"""
    console = Console()
    console.print(f"[blue]ℹ️  {message}[/blue]")

def confirm_action(message: str) -> bool:
    """Pide confirmación al usuario"""
    from rich.prompt import Confirm
    return Confirm.ask(message)

def get_user_input(prompt: str, default: str = None) -> str:
    """Obtiene entrada del usuario con valor por defecto"""
    from rich.prompt import Prompt
    if default:
        return Prompt.ask(prompt, default=default)
    return Prompt.ask(prompt)

def get_password_input(prompt: str) -> str:
    """Obtiene una contraseña del usuario"""
    from rich.prompt import Prompt
    return Prompt.ask(prompt, password=True)

def show_table(data: list, headers: list, title: str = None):
    """Muestra una tabla con los datos"""
    from rich.table import Table
    console = Console()
    
    table = Table(title=title)
    
    # Agregar columnas
    for header in headers:
        table.add_column(header, style="cyan")
    
    # Agregar filas
    for row in data:
        table.add_row(*[str(item) for item in row])
    
    console.print(table)

def show_progress(current: int, total: int, description: str = ""):
    """Muestra una barra de progreso"""
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=Console()
    ) as progress:
        task = progress.add_task(description, total=total)
        progress.update(task, completed=current)
