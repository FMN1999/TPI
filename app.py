import subprocess
import os


def run_backend():
    # Ruta al script de activación del entorno virtual
    activate_env = r'env\Scripts\activate.bat'

    # Ejecutar el backend de Django dentro del entorno virtual
    backend_command = f'{activate_env} && python backend/manage.py runserver'
    subprocess.Popen(backend_command, shell=True, cwd=os.getcwd())


def run_frontend():
    # Ejecutar el frontend de Angular con ng serve directamente
    frontend_command = ["ng", "serve"]
    process = subprocess.Popen(frontend_command, cwd="frontend/voley-app", shell=True)
    process.communicate()  # Asegura que el proceso se mantenga en ejecución


if __name__ == "__main__":
    print("Iniciando el backend Django...")
    run_backend()

    print("Iniciando el frontend Angular...")
    run_frontend()



