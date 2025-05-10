#!/bin/bash
# Iniciar la API Flask con el frontend
echo "Starting unified development server (Flask + Vite)..."

# Verificar si estamos en modo desarrollo
if [ "$NODE_ENV" == "production" ]; then
  # En producción, solo iniciamos Flask
  python api/app.py
else
  # En desarrollo, ejecutar el servidor integrado Flask + Vite
  python api/dev_server.py
fi