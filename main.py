# ...existing code...
from ui.app import run_app

def main():
    print("MAIN: start run_app()")
    try:
        run_app()
        print("MAIN: run_app() finished")
    except Exception as e:
        print("MAIN: exception en run_app():", e)

if __name__ == "__main__":
    main()