from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

def banner():    
    console.print(f"""
 ____  _____     _____  ___   ___  
/ ___||_   _|   |___  |/ _ \ / _ \ 
\___ \  | |        / /| | | | | | |
 ___) | | |       / / | |_| | |_| |
|____/  |_|      /_/   \___/ \___/
    """)
    show_copyright()

def show_copyright():
    license = "Todos los derechos reservados."
    autor = "PanaGaming"

    actual_year = datetime.now().year
    message = (
        f"[bold white]© {actual_year} {autor}[/bold white]\n"
        f"[dim white]{license}[/dim white]"
    )
    
    console.print(
        Panel(
            message,
            expand=False,
            border_style="blue",
            title="[bold blue]Copyright[/bold blue]",
            title_align="left"
        )
    )

def reloading_db():
    text = "[bold cyan]Reloading sqlite database...[/bold cyan]"
    console.print(text)
