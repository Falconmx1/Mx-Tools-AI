# banner.py
import pyfiglet
from termcolor import colored

def show_banner():
    banner_text = pyfiglet.figlet_format("Mx-Tools AI", font="slant")
    colored_banner = colored(banner_text, "red")
    print(colored_banner)
    print(colored("=" * 60, "cyan"))
    print(colored("  🔥 Cibernética Ofensiva/Defensiva | Ethical Red Team Suite", "yellow"))
    print(colored("  🛡️  Tres cabezas: Watcher | Attacker | Guardian", "green"))
    print(colored("  ⚠️  Solo para pruebas autorizadas. Uso ético obligatorio.", "red"))
    print(colored("=" * 60, "cyan"))
    print()

if __name__ == "__main__":
    show_banner()
