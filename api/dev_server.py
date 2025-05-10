#!/usr/bin/env python
# dev_server.py
# Script para iniciar un servidor de desarrollo Flask + Vite

import os
import sys
import subprocess
import threading
import time
import signal
import atexit

# Variables para controlar los procesos
vite_process = None
flask_process = None
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Función para ejecutar el servidor Vite
def run_vite():
    global vite_process
    try:
        os.chdir(os.path.join(root_dir, 'client'))
        # Primero construir la aplicación
        print("Construyendo la aplicación cliente...")
        subprocess.run(['npm', 'run', 'build'], check=True)
        
        # Copiar archivos construidos al directorio dist/public 
        dist_dir = os.path.join(root_dir, 'dist', 'public')
        os.makedirs(dist_dir, exist_ok=True)
        print(f"Copiando archivos construidos a {dist_dir}...")
        
        client_dist = os.path.join(root_dir, 'client', 'dist')
        if os.path.exists(client_dist):
            if os.name == 'nt':  # Windows
                subprocess.run(f'xcopy {client_dist} {dist_dir} /E /Y', shell=True)
            else:  # Unix/Linux/MacOS
                subprocess.run(f'cp -r {client_dist}/* {dist_dir}/', shell=True)
            print("Archivos copiados correctamente.")
        else:
            print("¡ADVERTENCIA! No se encontró el directorio dist del cliente")
        
        # Iniciar el servidor de desarrollo
        print("Iniciando servidor de desarrollo Vite...")
        vite_process = subprocess.Popen(['npm', 'run', 'dev'])
        
        # Para evitar que los procesos queden huérfanos en caso de salida abrupta
        def cleanup_vite():
            if vite_process and vite_process.poll() is None:
                print("Terminando proceso Vite...")
                if os.name == 'nt':  # Windows
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(vite_process.pid)])
                else:  # Unix/Linux/MacOS
                    vite_process.terminate()
                    vite_process.wait()

        atexit.register(cleanup_vite)
        return vite_process
    except Exception as e:
        print(f"Error ejecutando Vite: {e}")
        return None

# Función para ejecutar el servidor Flask
def run_flask():
    global flask_process
    try:
        os.chdir(os.path.join(root_dir, 'api'))
        print("Iniciando servidor Flask...")
        flask_process = subprocess.Popen(['python', 'app.py'])
        
        # Para evitar que los procesos queden huérfanos en caso de salida abrupta
        def cleanup_flask():
            if flask_process and flask_process.poll() is None:
                print("Terminando proceso Flask...")
                if os.name == 'nt':  # Windows
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(flask_process.pid)])
                else:  # Unix/Linux/MacOS
                    flask_process.terminate()
                    flask_process.wait()

        atexit.register(cleanup_flask)
        return flask_process
    except Exception as e:
        print(f"Error ejecutando Flask: {e}")
        return None

# Función para manejar la finalización del script
def signal_handler(sig, frame):
    print("Deteniendo servidores...")
    # Limpiar y terminar procesos
    if vite_process and vite_process.poll() is None:
        vite_process.terminate()
        vite_process.wait()
    if flask_process and flask_process.poll() is None:
        flask_process.terminate()
        flask_process.wait()
    sys.exit(0)

if __name__ == "__main__":
    print("Iniciando servidor de desarrollo unificado (Flask + Vite)")
    
    # Registrar el manejador de señales para CTRL+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Crear directorio dist si no existe
    dist_dir = os.path.join(root_dir, 'dist', 'public')
    os.makedirs(dist_dir, exist_ok=True)
    
    # Iniciar el servidor Vite en un hilo separado
    vite_thread = threading.Thread(target=run_vite)
    vite_thread.daemon = True
    vite_thread.start()
    
    print("Servidor Vite iniciado en segundo plano")
    time.sleep(5)  # Pausa para que Vite se inicie y termine la construcción
    
    # Iniciar el servidor Flask en el hilo principal
    flask_process = run_flask()
    
    # Mantener el script en ejecución
    try:
        while True:
            # Verificar que ambos procesos sigan en ejecución
            if vite_process and vite_process.poll() is not None:
                print("El proceso Vite ha terminado. Reiniciando...")
                vite_thread = threading.Thread(target=run_vite)
                vite_thread.daemon = True
                vite_thread.start()
            
            if flask_process and flask_process.poll() is not None:
                print("El proceso Flask ha terminado. Reiniciando...")
                flask_process = run_flask()
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Terminando servidores por solicitud de usuario...")
        signal_handler(signal.SIGINT, None)