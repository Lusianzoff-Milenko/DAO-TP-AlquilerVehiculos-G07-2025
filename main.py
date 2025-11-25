import sys
import os

# Asegura que el directorio raíz esté en el path para que funcionen los imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import run_app

def main():
    run_app()

if __name__ == "__main__":
    main()